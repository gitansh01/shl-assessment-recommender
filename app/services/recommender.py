from __future__ import annotations

from dataclasses import dataclass
import re
from typing import List, Optional, Tuple

from app.core.config import settings
from app.models.schemas import ChatRequest, ChatResponse, Recommendation, Message
from app.services.catalog import CatalogStore, Assessment, normalize_text
from app.services.comparison import compare_assessments
from app.services.guardrails import is_in_domain, is_prompt_injection
from app.services.retrieval import EmbeddingIndex


@dataclass
class IntentResult:
    intent: str
    role: str
    skills: List[str]
    seniority: str
    test_types: List[str]
    compare_names: List[str]
    clarification_question: str


class IntentExtractor:
    ROLE_PREFIXES = [
        "hiring",
        "looking for",
        "need",
        "seeking",
        "recruiting",
        "searching for",
    ]
    ROLE_STOPWORDS = ["with", "who", "that", "for", "to", "and", "including", "requiring"]
    SENIORITY_KEYWORDS = [
        "entry-level",
        "entry level",
        "junior",
        "mid",
        "mid-level",
        "senior",
        "lead",
        "manager",
        "director",
        "executive",
    ]
    TEST_TYPE_WORDS = [
        "personality",
        "cognitive",
        "behavioral",
        "skills",
        "simulation",
        "situational",
        "aptitude",
        "knowledge",
    ]
    SKILL_PATTERNS = [
        r"skills?\s+in\s+(?P<skills>[^.;]+)",
        r"with\s+(?P<skills>[^.;]+?)\s+skills?",
        r"experience\s+in\s+(?P<skills>[^.;]+)",
        r"knowledge\s+of\s+(?P<skills>[^.;]+)",
        r"proficient\s+in\s+(?P<skills>[^.;]+)",
    ]
    COMPARE_PATTERN = re.compile(r"\b(compare|difference|vs|versus)\b", re.IGNORECASE)
    TEST_TYPE_PATTERN = re.compile(r"\b(test type|type)\s*[:\-]?\s*([A-Z](?:\s*[A-Z])*)\b")

    def __init__(self, catalog: CatalogStore) -> None:
        self.catalog = catalog
        self.name_lookup = {
            normalize_text(name): name for name in catalog.all_names() if name
        }

    def extract(self, messages: List[Message]) -> IntentResult:
        role = ""
        skills: List[str] = []
        seniority = ""
        test_types: List[str] = []
        compare_names: List[str] = []
        compare_triggered = False

        for message in [m for m in messages if m.role == "user"]:
            text = message.content
            if self.COMPARE_PATTERN.search(text):
                compare_triggered = True
                compare_names = self._merge_list(
                    compare_names, self._find_assessment_names(text) or self._split_compare_parts(text)
                )
            new_role = self._extract_role(text)
            if new_role:
                role = new_role
            skills = self._merge_list(skills, self._extract_skills(text))
            new_seniority = self._extract_seniority(text)
            if new_seniority:
                seniority = new_seniority
            test_types = self._merge_list(test_types, self._extract_test_types(text))

        intent = "recommend"
        clarification_question = ""
        if compare_triggered:
            intent = "compare"
        elif not role:
            intent = "clarify"
            clarification_question = "What role are you hiring for?"
        elif not skills:
            intent = "clarify"
            clarification_question = "Which key skills should the assessment cover?"

        return IntentResult(
            intent=intent,
            role=role,
            skills=skills,
            seniority=seniority,
            test_types=test_types,
            compare_names=compare_names,
            clarification_question=clarification_question,
        )

    def _extract_role(self, text: str) -> str:
        lowered = text.lower()
        for prefix in self.ROLE_PREFIXES:
            if prefix in lowered:
                after = lowered.split(prefix, 1)[1].strip()
                for stop in self.ROLE_STOPWORDS:
                    if f" {stop} " in after:
                        after = after.split(f" {stop} ", 1)[0].strip()
                return after.title()
        if "role:" in lowered:
            return lowered.split("role:", 1)[1].strip().split(".")[0].title()
        return ""

    def _extract_skills(self, text: str) -> List[str]:
        matches: List[str] = []
        for pattern in self.SKILL_PATTERNS:
            found = re.search(pattern, text, flags=re.IGNORECASE)
            if found:
                matches.extend(self._split_list(found.group("skills")))
        return matches

    def _extract_seniority(self, text: str) -> str:
        lowered = text.lower()
        for keyword in self.SENIORITY_KEYWORDS:
            if keyword in lowered:
                return keyword.replace("-", " ").title()
        return ""

    def _extract_test_types(self, text: str) -> List[str]:
        types: List[str] = []
        match = self.TEST_TYPE_PATTERN.search(text)
        if match:
            letters = re.findall(r"[A-Z]", match.group(2).upper())
            types.extend(letters)
        lowered = text.lower()
        for word in self.TEST_TYPE_WORDS:
            if f"{word} test" in lowered:
                types.append(word)
        return types

    def _find_assessment_names(self, text: str) -> List[str]:
        normalized = normalize_text(text)
        return [
            name
            for key, name in self.name_lookup.items()
            if key and key in normalized
        ]

    def _split_compare_parts(self, text: str) -> List[str]:
        parts = re.split(r"\bvs\b|\bversus\b|difference between|compare", text, flags=re.IGNORECASE)
        return [part.strip(" ,.?") for part in parts if part.strip(" ,.?")]

    @staticmethod
    def _split_list(value: str) -> List[str]:
        parts = re.split(r",|/|&|\band\b", value, flags=re.IGNORECASE)
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _merge_list(existing: List[str], new_items: List[str]) -> List[str]:
        results = list(existing)
        for item in new_items:
            if item not in results:
                results.append(item)
        return results


class ChatRecommender:
    def __init__(self, catalog: CatalogStore, vector_index: Optional[EmbeddingIndex]) -> None:
        self.catalog = catalog
        self.vector_index = vector_index
        self.intent_extractor = IntentExtractor(catalog)

    def handle_chat(self, request: ChatRequest) -> ChatResponse:
        if not request.messages:
            return ChatResponse(
                reply="Please provide at least one user message.",
                recommendations=[],
                end_of_conversation=False,
            )

        user_turns = sum(1 for m in request.messages if m.role == "user")
        if user_turns > settings.MAX_TURNS:
            return ChatResponse(
                reply="This conversation has reached the maximum of 8 user turns. Please start a new request.",
                recommendations=[],
                end_of_conversation=True,
            )

        last_user = self._last_user_message(request.messages)
        if not last_user:
            return ChatResponse(
                reply="Please send a user message to continue.",
                recommendations=[],
                end_of_conversation=False,
            )

        if is_prompt_injection(last_user.content):
            return self._refusal()

        in_domain = is_in_domain(last_user.content, self.catalog.is_known_name(last_user.content))
        if not in_domain:
            return self._refusal()

        if self.catalog.is_empty():
            return ChatResponse(
                reply="The SHL catalog has not been loaded yet. Run the scraping and indexing scripts first.",
                recommendations=[],
                end_of_conversation=True,
            )

        intent = self.intent_extractor.extract(request.messages)
        if intent.intent == "refuse":
            return self._refusal()
        if intent.intent == "compare":
            return self._handle_compare(intent)
        if intent.intent == "clarify":
            question = self._clarification_question(intent)
            return ChatResponse(reply=question, recommendations=[], end_of_conversation=False)

        return self._handle_recommend(intent, last_user.content)

    def _handle_compare(self, intent: IntentResult) -> ChatResponse:
        items = self.catalog.resolve_names(intent.compare_names)
        if len(items) < 2:
            return ChatResponse(
                reply="Which two SHL assessments should I compare?",
                recommendations=[],
                end_of_conversation=False,
            )
        left, right = items[0], items[1]
        reply = compare_assessments(left, right)
        return ChatResponse(reply=reply, recommendations=[], end_of_conversation=False)

    def _handle_recommend(self, intent: IntentResult, last_user_text: str) -> ChatResponse:
        query_text = self._build_query(intent, last_user_text)
        ranked = self._rank_candidates(query_text)
        if intent.test_types:
            ranked = [item for item in ranked if self._matches_test_type(item, intent.test_types)]
        if not ranked:
            question = self._clarification_question(intent)
            return ChatResponse(reply=question, recommendations=[], end_of_conversation=False)
        max_count = min(settings.DEFAULT_RECOMMENDATION_COUNT, settings.MAX_RECOMMENDATIONS)
        selected = ranked[:max_count]
        reply = self._format_recommendation_reply(intent, selected)
        return ChatResponse(
            reply=reply,
            recommendations=[self._to_recommendation(item) for item in selected],
            end_of_conversation=False,
        )

    def _rank_candidates(self, query_text: str) -> List[Assessment]:
        if self.vector_index:
            results = self.vector_index.search(query_text, settings.TOP_K)
            ranked = []
            for item_id, _score in results:
                item = self.catalog.get_by_id(item_id)
                if item:
                    ranked.append(item)
            if ranked:
                return ranked
        return self._keyword_rank(query_text)

    def _keyword_rank(self, query_text: str) -> List[Assessment]:
        tokens = set(normalize_text(query_text).split())
        scored: List[Tuple[Assessment, int]] = []
        for item in self.catalog.items:
            haystack = " ".join(
                [
                    item.name,
                    item.description,
                    item.test_type,
                    " ".join(item.skills),
                    " ".join(item.job_family),
                    " ".join(item.job_levels),
                ]
            )
            hay_tokens = set(normalize_text(haystack).split())
            score = len(tokens.intersection(hay_tokens))
            if score > 0:
                scored.append((item, score))
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [item for item, _score in scored]

    def _matches_test_type(self, item: Assessment, test_types: List[str]) -> bool:
        haystack = normalize_text(" ".join([item.test_type, item.description]))
        for value in test_types:
            if normalize_text(value) in haystack:
                return True
        return False

    def _build_query(self, intent: IntentResult, last_user_text: str) -> str:
        parts = [
            intent.role,
            intent.seniority,
            " ".join(intent.skills),
            " ".join(intent.test_types),
            last_user_text,
        ]
        return " | ".join([part for part in parts if part])

    def _format_recommendation_reply(self, intent: IntentResult, items: List[Assessment]) -> str:
        context_parts = []
        if intent.role:
            context_parts.append(f"the {intent.role} role")
        if intent.skills:
            context_parts.append(f"skills in {', '.join(intent.skills)}")
        if context_parts:
            context = " and ".join(context_parts)
            return f"Based on {context}, here are suitable SHL assessments from the catalog."
        return "Here are suitable SHL assessments from the catalog."

    def _clarification_question(self, intent: IntentResult) -> str:
        if intent.clarification_question:
            return intent.clarification_question
        if not intent.role:
            return "What role are you hiring for?"
        if not intent.skills:
            return "Which key skills should the assessment cover?"
        return "Could you share more details about the role and required skills?"

    def _to_recommendation(self, item: Assessment) -> Recommendation:
        return Recommendation(name=item.name, url=item.url, test_type=item.test_type)

    def _refusal(self) -> ChatResponse:
        return ChatResponse(
            reply="I can only help with SHL individual test assessments from the product catalog.",
            recommendations=[],
            end_of_conversation=False,
        )

    @staticmethod
    def _last_user_message(messages: List[Message]) -> Optional[Message]:
        for message in reversed(messages):
            if message.role == "user":
                return message
        return None

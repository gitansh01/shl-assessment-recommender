from __future__ import annotations

import re

INJECTION_PATTERNS = [
    r"ignore (all|previous|prior) instructions",
    r"system prompt",
    r"developer message",
    r"jailbreak",
    r"act as",
    r"roleplay",
    r"bypass",
    r"prompt injection",
]

DOMAIN_KEYWORDS = [
    "assessment",
    "assessments",
    "test",
    "testing",
    "candidate",
    "hiring",
    "hire",
    "role",
    "job",
    "skills",
    "psychometric",
    "aptitude",
    "personality",
    "shl",
]


def is_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in INJECTION_PATTERNS)


def is_in_domain(text: str, has_known_assessment: bool) -> bool:
    lowered = text.lower()
    if has_known_assessment:
        return True
    return any(keyword in lowered for keyword in DOMAIN_KEYWORDS)

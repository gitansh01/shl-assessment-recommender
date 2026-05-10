from __future__ import annotations

from app.services.catalog import Assessment


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "Not specified"


def compare_assessments(left: Assessment, right: Assessment) -> str:
    parts = [
        f"{left.name} vs {right.name}:",
        f"- Test type: {left.test_type or 'Not specified'} vs {right.test_type or 'Not specified'}",
        f"- Typical duration: {left.duration_minutes or 'Not specified'} vs {right.duration_minutes or 'Not specified'}",
        f"- Skills: {format_list(left.skills)} vs {format_list(right.skills)}",
        f"- Job families: {format_list(left.job_family)} vs {format_list(right.job_family)}",
        f"- Description (left): {left.description or 'Not specified'}",
        f"- Description (right): {right.description or 'Not specified'}",
    ]
    return "\n".join(parts)

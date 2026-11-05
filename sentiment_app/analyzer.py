"""Score a short Kazakh or Russian comment about a national policy.

The thesis picked Gemini 3.5 Flash for this task. This service is the local
scorer that the lab can run in CI without an API key. The word lists are the
same ones used in the coursework demo of that project.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

NEGATIVE_PHRASES = (
    "дұрыс емес",
    "ауыр",
    "кешіг",
    "наразы",
    "қарсы",
    "жетпейді",
    "лишн",
    "тяжело",
    "плохо",
    "против",
    "ужасно",
    "не надо",
)
POSITIVE_PHRASES = (
    "ыңғайлы",
    "қолдаймын",
    "ризамын",
    "рахмет",
    "жақсы",
    "дұрыс",
    "удобно",
    "поддерживаю",
    "хорошо",
)
TOPIC_CUES = (
    ("mobile_transfer_tax", "Mobile transfer tax", ("аударым", "перевод")),
    ("egov_identity", "eGov mobile identity", ("egov", "еgov", "куәлік", "құжат", "документ")),
    ("school_construction", "School construction", ("мектеп", "школ")),
    ("pension_indexation", "Pension indexation", ("зейнетақы", "пенси")),
)


@dataclass(frozen=True)
class SentimentResult:
    label: str
    confidence: float
    topic: str
    topic_label: str

    def as_dict(self) -> dict:
        return asdict(self)


def analyze_comment(text: str) -> SentimentResult:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Comment text is empty.")
    if len(cleaned) > 2000:
        raise ValueError("Comment exceeds 2000 characters.")

    folded = cleaned.casefold()
    negative, rest = _consume(folded, NEGATIVE_PHRASES)
    positive, _rest = _consume(rest, POSITIVE_PHRASES)
    topic, topic_label = _topic(folded)

    if negative > positive:
        label = "negative"
    elif positive > negative:
        label = "positive"
    else:
        label = "neutral"

    margin = abs(positive - negative)
    confidence = 0.56 if margin == 0 else min(0.93, 0.64 + 0.09 * margin)
    return SentimentResult(label, round(confidence, 2), topic, topic_label)


def _consume(text: str, phrases: tuple[str, ...]) -> tuple[int, str]:
    remaining = text
    count = 0
    for phrase in sorted(phrases, key=len, reverse=True):
        found = remaining.count(phrase)
        if found:
            count += found
            remaining = remaining.replace(phrase, " ")
    return count, remaining


def _topic(folded: str) -> tuple[str, str]:
    best_key = "general_policy"
    best_label = "General policy"
    best_hits = 0
    for key, label, cues in TOPIC_CUES:
        hits = sum(folded.count(cue) for cue in cues)
        if hits > best_hits:
            best_key, best_label, best_hits = key, label, hits
    return best_key, best_label

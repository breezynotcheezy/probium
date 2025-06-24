import math


def score_magic(length: int) -> float:
    """Return confidence score based on magic signature length."""
    if length <= 0:
        return 0.5
    score = 1 - math.exp(-length / 4.0)
    return round(min(score, 1.0), 2)


def score_tokens(ratio: float) -> float:
    """Return confidence score based on token match ratio."""
    ratio = max(0.0, min(ratio, 1.0))
    if ratio == 0:
        return 0.5
    if ratio >= 0.1:
        return 1.0
    score = 0.8 + 2 * ratio
    return round(min(score, 1.0), 2)

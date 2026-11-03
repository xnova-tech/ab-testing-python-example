from dataclasses import dataclass
from math import erfc, sqrt


@dataclass(frozen=True, slots=True)
class SRMResult:
    chi_square: float
    p_value: float
    mismatch_detected: bool


def check_srm_50_50(users_a: int, users_b: int, alpha: float = 0.001) -> SRMResult:
    """Check assignment counts against a planned 50/50 split."""
    for name, value in (("users_a", users_a), ("users_b", users_b)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        if value < 0:
            raise ValueError(f"{name} must be non-negative")
    if users_a + users_b == 0:
        raise ValueError("at least one assigned user is required")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between zero and one")

    expected = (users_a + users_b) / 2
    chi_square = (users_a - expected) ** 2 / expected + (users_b - expected) ** 2 / expected
    # With two variants the chi-square statistic has one degree of freedom.
    p_value = erfc(sqrt(chi_square / 2))
    return SRMResult(chi_square, p_value, p_value < alpha)

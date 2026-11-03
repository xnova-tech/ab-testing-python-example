from dataclasses import dataclass
from math import erfc, sqrt
from statistics import NormalDist


def _require_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")


@dataclass(frozen=True, slots=True)
class ExperimentGroup:
    users: int
    conversions: int

    def __post_init__(self) -> None:
        _require_integer("users", self.users)
        _require_integer("conversions", self.conversions)
        if self.users <= 0:
            raise ValueError("users must be positive")
        if self.conversions < 0:
            raise ValueError("conversions must be non-negative")
        if self.conversions > self.users:
            raise ValueError("conversions cannot exceed users")

    @property
    def conversion_rate(self) -> float:
        return self.conversions / self.users


@dataclass(frozen=True, slots=True)
class ABResult:
    rate_a: float
    rate_b: float
    absolute_change: float
    relative_change: float
    pooled_probability: float
    z_statistic: float
    p_value: float
    ci_95_low: float
    ci_95_high: float


def calculate_ab_test(group_a: ExperimentGroup, group_b: ExperimentGroup) -> ABResult:
    rate_a = group_a.conversion_rate
    rate_b = group_b.conversion_rate
    difference = rate_b - rate_a
    if rate_a == 0:
        raise ValueError("relative change is undefined for a zero baseline")

    pooled = (group_a.conversions + group_b.conversions) / (group_a.users + group_b.users)
    test_se = sqrt(pooled * (1 - pooled) * (1 / group_a.users + 1 / group_b.users))
    z_statistic = difference / test_se if test_se else 0.0
    p_value = erfc(abs(z_statistic) / sqrt(2))

    # Wald interval: unlike the null-hypothesis test, this SE is not pooled.
    interval_se = sqrt(rate_a * (1 - rate_a) / group_a.users + rate_b * (1 - rate_b) / group_b.users)
    margin = NormalDist().inv_cdf(0.975) * interval_se

    return ABResult(
        rate_a=rate_a,
        rate_b=rate_b,
        absolute_change=difference,
        relative_change=difference / rate_a,
        pooled_probability=pooled,
        z_statistic=z_statistic,
        p_value=p_value,
        ci_95_low=difference - margin,
        ci_95_high=difference + margin,
    )


def main() -> None:
    group_a = ExperimentGroup(users=1000, conversions=120)
    group_b = ExperimentGroup(users=1000, conversions=160)
    result = calculate_ab_test(group_a, group_b)
    print(f"a_conversion_percent: {result.rate_a * 100:.2f}")
    print(f"b_conversion_percent: {result.rate_b * 100:.2f}")
    print(f"absolute_change_pp: {result.absolute_change * 100:.2f}")
    print(f"relative_change_percent: {result.relative_change * 100:.2f}")
    print(f"pooled_probability: {result.pooled_probability:.4f}")
    print(f"z_statistic: {result.z_statistic:.6f}")
    print(f"p_value: {result.p_value:.6f}")
    print(f"ci_95_low_pp: {result.ci_95_low * 100:.2f}")
    print(f"ci_95_high_pp: {result.ci_95_high * 100:.2f}")


if __name__ == "__main__":
    main()

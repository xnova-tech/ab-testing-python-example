from typing import cast

import pytest

from ab_test_calculation import ABResult, ExperimentGroup, calculate_ab_test


@pytest.fixture
def result() -> ABResult:
    group_a = ExperimentGroup(users=1000, conversions=120)
    group_b = ExperimentGroup(users=1000, conversions=160)
    return calculate_ab_test(group_a, group_b)


def test_calculation_matches_synthetic_example(result: ABResult) -> None:
    assert result.rate_a == pytest.approx(0.12)
    assert result.rate_b == pytest.approx(0.16)
    assert result.pooled_probability == pytest.approx(0.14)
    assert result.z_statistic == pytest.approx(2.577696, abs=1e-6)
    assert result.p_value == pytest.approx(0.009946, abs=1e-6)
    assert result.ci_95_low == pytest.approx(0.0096, abs=5e-5)
    assert result.ci_95_high == pytest.approx(0.0704, abs=5e-5)


def test_absolute_and_relative_changes_use_different_units(result: ABResult) -> None:
    assert result.absolute_change * 100 == pytest.approx(4.0)
    assert result.relative_change * 100 == pytest.approx(100 / 3)


@pytest.mark.parametrize(
    ("users", "conversions", "error_type", "message"),
    [
        (0, 0, ValueError, "users must be positive"),
        (-1, 0, ValueError, "users must be positive"),
        (1000, -1, ValueError, "conversions must be non-negative"),
        (1000, 1001, ValueError, "conversions cannot exceed users"),
        (cast(int, 1000.5), 120, TypeError, "users must be an integer"),
        (1000, cast(int, "120"), TypeError, "conversions must be an integer"),
        (cast(int, True), 1, TypeError, "users must be an integer"),
    ],
)
def test_group_rejects_invalid_counts(
    users: int,
    conversions: int,
    error_type: type[Exception],
    message: str,
) -> None:
    with pytest.raises(error_type, match=message):
        ExperimentGroup(users=users, conversions=conversions)


def test_equal_conversion_rates_have_neutral_statistic() -> None:
    result = calculate_ab_test(
        ExperimentGroup(users=1000, conversions=120),
        ExperimentGroup(users=500, conversions=60),
    )

    assert result.z_statistic == pytest.approx(0.0)
    assert result.p_value == pytest.approx(1.0)


def test_zero_baseline_rejects_relative_change() -> None:
    with pytest.raises(ValueError, match="relative change is undefined"):
        calculate_ab_test(
            ExperimentGroup(users=1000, conversions=0),
            ExperimentGroup(users=1000, conversions=10),
        )

from typing import cast

import pytest

from srm_check import check_srm_50_50


def test_balanced_allocation_has_no_mismatch() -> None:
    result = check_srm_50_50(1000, 1000)

    assert result.chi_square == pytest.approx(0.0)
    assert result.p_value == pytest.approx(1.0)
    assert not result.mismatch_detected


def test_obvious_skew_is_detected() -> None:
    result = check_srm_50_50(650, 350)

    assert result.p_value < 0.001
    assert result.mismatch_detected


@pytest.mark.parametrize("users", [-1, cast(int, 1000.5), cast(int, True)])
def test_invalid_allocation_is_rejected(users: int) -> None:
    with pytest.raises((TypeError, ValueError)):
        check_srm_50_50(users, 1000)


def test_empty_allocation_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least one assigned user"):
        check_srm_50_50(0, 0)


@pytest.mark.parametrize("alpha", [0.0, 1.0, -0.1, 1.1])
def test_invalid_alpha_is_rejected(alpha: float) -> None:
    with pytest.raises(ValueError, match="alpha must be between zero and one"):
        check_srm_50_50(1000, 1000, alpha=alpha)

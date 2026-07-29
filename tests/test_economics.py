# Basic pytest-based unit tests for nomos_sim.economics

from nomos_sim import economics
import math


def test_decimal_scarcity_basic():
    # If X+Y == 100 -> int_part=100 -> N=3 -> r_s = 1 / 2^(3-2) = 1/2
    r = economics.decimal_scarcity(60, 40)
    assert math.isclose(r, 0.5, rel_tol=1e-9)


def test_decimal_scarcity_small_total():
    # For small totals (<1) we clamp N to 2 so r_s == 1.0
    r = economics.decimal_scarcity(0.0, 0.0)
    # With our clamp N=2 -> r_s = 1 / 2^(2-2) = 1
    assert math.isclose(r, 1.0, rel_tol=1e-9)


def test_elastic_velocity_coefficient_clamp():
    # If V_T >> V_A then C_V should be clamped to max (2.0)
    cv = economics.elastic_velocity_coefficient(10.0, 0.001)
    assert math.isclose(cv, 2.0, rel_tol=1e-9)


def test_mint_and_split_reward():
    v_tx = 50.0
    X = 1000.0
    Y = 500000.0
    V_T = 1.0
    V_A = 0.5
    R = economics.mint_reward(v_tx, X, Y, V_T, V_A)
    s, rcv, n = economics.split_reward(R)
    assert math.isclose(s + rcv + n, R, rel_tol=1e-9)


def test_dynamic_daily_cap():
    assert economics.dynamic_daily_cap(0.03) == 30.0

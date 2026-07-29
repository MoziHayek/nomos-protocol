"""Economic formulas extracted from Nomos whitepaper.

Functions provided:
- decimal_scarcity(X, Y)
- elastic_velocity_coefficient(V_T, V_A, eps=1e-9, min_cv=0.5, max_cv=2.0)
- mint_reward(v_tx, X, Y, V_T, V_A, eps=1e-9)
- split_reward(R)
- dynamic_daily_cap(R_total)

The implementations follow the whitepaper formulas with small, explicit
safeguards (e.g., minimum digit count) so results are stable for edge cases
used in simulations.
"""
from typing import Tuple

import math


def decimal_scarcity(X: float, Y: float) -> float:
    """Decimal Scarcity Algorithm.

    Whitepaper: N = number of decimal digits in (X + Y)
    r_s = 1 / 2^(N-2)

    To avoid negative exponents for tiny X+Y, this implementation clamps
    the digit count to a minimum of 2 (so r_s <= 1).

    Args:
        X: total transaction volume (e.g., last 30 days)
        Y: circulating supply

    Returns:
        scarcity factor r_s (0 < r_s <= 1)
    """
    total = max(0.0, float(X + Y))
    # Determine number of decimal digits in integer part
    # If total is 0, treat as 1 to avoid log10 domain error
    int_part = int(math.floor(total)) if total >= 1.0 else 0
    if int_part > 0:
        N = len(str(int_part))
    else:
        # For totals < 1, treat as 1 digit to keep formula stable
        N = 1
    # Clamp N to minimum of 2 to prevent r_s > 1
    N = max(N, 2)
    r_s = 1.0 / (2 ** (N - 2))
    return r_s


def elastic_velocity_coefficient(
    V_T: float, V_A: float, eps: float = 1e-9, min_cv: float = 0.5, max_cv: float = 2.0
) -> float:
    """Elastic Velocity Stimulus coefficient C_V.

    Whitepaper: C_V = V_T / max(V_A, eps)
    Clamped between bounds (default 0.5 and 2.0).

    Args:
        V_T: target velocity
        V_A: actual velocity
        eps: small epsilon to avoid division by zero
        min_cv, max_cv: clamp bounds

    Returns:
        clamped C_V
    """
    denom = max(V_A, eps)
    cv = V_T / denom
    cv = max(min_cv, min(max_cv, cv))
    return cv


def mint_reward(
    v_tx: float, X: float, Y: float, V_T: float, V_A: float, eps: float = 1e-9
) -> float:
    """Complete minting formula R = v_tx * r_s * C_V

    Args:
        v_tx: transaction value
        X: total transaction volume (for scarcity)
        Y: circulating supply (for scarcity)
        V_T: target velocity
        V_A: actual velocity
        eps: epsilon passed to elastic coefficient

    Returns:
        R: minted reward for the transaction
    """
    r_s = decimal_scarcity(X, Y)
    C_V = elastic_velocity_coefficient(V_T, V_A, eps)
    R = v_tx * r_s * C_V
    return R


def split_reward(R: float) -> Tuple[float, float, float]:
    """Split reward equally between sender, receiver, and node (1/3 each).

    Returns (sender_share, receiver_share, node_share).
    """
    share = R / 3.0
    return (share, share, share)


def dynamic_daily_cap(R_total: float) -> float:
    """Dynamic daily cap per wallet: C_wallet = 1000 * R_total

    Args:
        R_total: total protocol-wide reward rate for the epoch (e.g., 0.03 for 3%)
    Returns:
        absolute UNITT ceiling per 24-hour epoch
    """
    return 1000.0 * float(R_total)

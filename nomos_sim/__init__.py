"""Nomos Protocol simulation helpers

This small library extracts key whitepaper formulas (Decimal Scarcity Algorithm,
Elastic Velocity Stimulus, minting formula, and daily cap) for use in
simulations and tests.
"""

__version__ = "0.1.0"

from .economics import (
    decimal_scarcity,
    elastic_velocity_coefficient,
    mint_reward,
    split_reward,
    dynamic_daily_cap,
)

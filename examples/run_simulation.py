"""Example simulation script for Nomos Protocol formulas.

This script uses the nomos_sim library to run a 12-month simulation and
produce a CSV and PNG showing daily market volume, minted reward, and total
supply over time.

Run:
    python examples/run_simulation.py

Outputs:
    nomos_example.csv  -- daily rows: day,month,daily_volume,R,supply
    nomos_example.png  -- plot of daily volume and supply over time

This example is intentionally simple and intended to demonstrate how to use
nomos_sim.economics functions in a repeatable simulation.
"""

import csv
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from nomos_sim.economics import (
    decimal_scarcity,
    elastic_velocity_coefficient,
    mint_reward,
    split_reward,
    dynamic_daily_cap,
)

OUTPUT_CSV = "nomos_example.csv"
OUTPUT_PNG = "nomos_example.png"


def run_simulation(seed: int = 42):
    np.random.seed(seed)

    # Initial protocol state
    supply = 1_000_000.0
    V_T = 1.0  # target velocity

    days_total = 12 * 30
    records = []

    # We'll maintain a running X (30-day window total volume) for scarcity
    rolling_window = []

    day_index = 0
    for month in range(12):
        base_vol = 1.5 if month < 6 else 0.5
        daily_volumes = np.random.normal(base_vol, 0.2, 30)
        # ensure non-negative volumes
        daily_volumes = np.clip(daily_volumes, 0.0, None)

        monthly_vol = float(np.sum(daily_volumes))

        # Simple heuristic for actual velocity used in examples (match VE_12_M)
        V_A = (monthly_vol * 10) / (supply / 100_000)
        # clamp to a small epsilon for safety in the coefficient function
        C_V = elastic_velocity_coefficient(V_T, V_A)

        # rolling window X for scarcity: sum of last 30 days (for simplicity use monthly_vol)
        X = monthly_vol

        for d in daily_volumes:
            # Use current rolling totals as inputs
            r_s = decimal_scarcity(X, supply)
            R = mint_reward(d, X, supply, V_T, V_A)
            sender, receiver, node = split_reward(R)

            supply += R

            records.append(
                {
                    "day": day_index,
                    "month": month,
                    "daily_volume": float(d),
                    "r_s": float(r_s),
                    "C_V": float(C_V),
                    "R": float(R),
                    "sender": float(sender),
                    "receiver": float(receiver),
                    "node": float(node),
                    "supply": float(supply),
                }
            )

            day_index += 1

    # Write CSV
    fieldnames = [
        "day",
        "month",
        "daily_volume",
        "r_s",
        "C_V",
        "R",
        "sender",
        "receiver",
        "node",
        "supply",
    ]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(r)

    # Plot results
    days = [r["day"] for r in records]
    volumes = [r["daily_volume"] for r in records]
    supplies = [r["supply"] for r in records]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(days, volumes, color="gray", alpha=0.6, label="daily_volume")
    ax1.set_ylabel("Daily Volume", color="gray")
    ax1.tick_params(axis="y", labelcolor="gray")

    ax2 = ax1.twinx()
    ax2.plot(days, supplies, color="green", label="supply")
    ax2.set_ylabel("Supply", color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    plt.title("Nomos Example Simulation ({})".format(datetime.utcnow().isoformat()))
    ax1.set_xlabel("Day")

    # Save plot
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150)
    print(f"Wrote {OUTPUT_CSV} and {OUTPUT_PNG}")


if __name__ == "__main__":
    run_simulation()

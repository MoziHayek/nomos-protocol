import numpy as np
import matplotlib.pyplot as plt

def simulate_nomos_30_day_cycle():
    # Initial State
    supply = 1_000_000
    cv = 1.0  # Multiplier starts at neutral
    history_cv, history_supply, history_vol = [], [], []
    
    # 12 Months of simulation
    for month in range(12):
        # Generate 30 days of "Market Activity" (Jagged/Real-world data)
        # Month 1-6: Strong Growth | Month 7-12: Stagnation/Hoarding
        base_vol = 1.5 if month < 6 else 0.5
        daily_volumes = np.random.normal(base_vol, 0.2, 30)
        
        # Monthly Totals
        monthly_vol = np.sum(daily_volumes)
        
        # DAILY LOOP (Within the month, Cv is LOCKED)
        for d_vol in daily_volumes:
            # Rewards are minted based on the Cv set by the PREVIOUS month
            minted = d_vol * cv * 100 
            supply += minted
            
            history_cv.append(cv)
            history_supply.append(supply)
            history_vol.append(d_vol)

        # END OF MONTH: Reassess Multiplier for the NEXT 30 days
        # Ratio of Volume/Supply (Simplified for logic)
        ratio = (monthly_vol * 10) / (supply / 100_000)
        
        # Cybernetic Adjustment: Targeting a ratio of ~1.0
        # If the ratio is high, Cv goes up (stimulate motion). 
        # If low, Cv goes down (cool inflation).
        cv = np.clip(cv * (ratio / 1.0), 0.5, 2.0)

    return history_cv, history_supply, history_vol

# Run and Plot
cv_data, supply_data, vol_data = simulate_nomos_30_day_cycle()

plt.figure(figsize=(10, 6))
plt.step(range(360), cv_data, where='post', color='blue', label='Epoch Multiplier (Cv)')
plt.plot(vol_data, alpha=0.2, color='gray', label='Daily Market Noise')
plt.title('Nomos 30-Day Epoch: Cybernetic "Heartbeat" Logic')
plt.ylabel('Multiplier (Cv)')
plt.xlabel('Days')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

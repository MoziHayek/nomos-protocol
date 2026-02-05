import numpy as np
import matplotlib.pyplot as plt

def simulate_nomos_inverse_logic():
    # Parameters
    supply = 1_000_000
    target_v = 1.0  # The "ideal" motion the protocol wants
    cv = 1.0        # Initial Multiplier
    
    days = 360
    history_v, history_cv, history_supply = [], [], []
    
    # 12 Months of simulation
    for month in range(12):
        # Scenario: Economy starts active, then enters a 6-month recession
        if month < 3:
            monthly_activity = np.random.normal(1.2, 0.1, 30) # High Velocity
        elif month < 9:
            monthly_activity = np.random.normal(0.4, 0.05, 30) # "The Stagnation"
        else:
            monthly_activity = np.random.normal(0.8, 0.1, 30) # Recovery
            
        # 1. DAILY LOOP (Cv is fixed for the 30-day Epoch)
        for daily_v in monthly_activity:
            # Minting = (Base) * Cv
            # Note: High Cv during stagnation increases supply to "push" motion
            minted = 100 * cv 
            supply += minted
            
            history_v.append(daily_v)
            history_cv.append(cv)
            history_supply.append(supply)
            
        # 2. EPOCH REASSESSMENT (Day 31)
        # Formula: Cv_next = Target_V / Actual_V
        actual_v = np.mean(monthly_activity)
        
        # We apply the clamp here to prevent infinite minting if v -> 0
        cv = np.clip(target_v / actual_v, 0.5, 2.5)

    return history_v, history_cv, history_supply

v_data, cv_data, supply_data = simulate_nomos_inverse_logic()

# Plotting the results
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax1.plot(v_data, color='gray', alpha=0.3, label='Daily Velocity (V)')
ax1.step(range(360), cv_data, where='post', color='red', label='Multiplier (Cv)')
ax1.set_title('Nomos Inverse Cybernetics: Stagnation triggers Stimulus')
ax1.legend()

ax2.plot(supply_data, color='green')
ax2.set_title('Total Supply Response')
ax2.set_ylabel('Tokens in Circulation')
plt.show()

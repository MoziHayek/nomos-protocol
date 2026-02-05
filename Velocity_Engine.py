import numpy as np
import matplotlib.pyplot as plt

def calculate_cv(velocity, target_v=1.0, clamp=2.0):
    """
    Simulates the Nomos Velocity Multiplier (Cv).
    Responds to Economic Motion (V) and caps at the safety limit.
    """
    # Using a logistic growth curve to simulate organic cybernetic scaling
    cv = clamp / (1 + np.exp(-1.5 * (velocity - target_v)))
    return np.round(cv, 4)

# 1. Generate a range of Transaction Velocities
velocities = np.linspace(0, 5, 100)
cv_values = [calculate_cv(v) for v in velocities]

# 2. Model the Tri-Symmetric Reward Split (33/33/33)
base_reward = 100 
total_rewards = np.array(cv_values) * base_reward
sender_share = total_rewards / 3
receiver_share = total_rewards / 3
node_share = total_rewards / 3

# 3. Visualization
plt.figure(figsize=(10, 5))

# Plot A: The Velocity Response
plt.subplot(1, 2, 1)
plt.plot(velocities, cv_values, color='blue', lw=2)
plt.axhline(y=2.0, color='red', linestyle='--', label='Safety Clamp (2.0)')
plt.title('Cybernetic Velocity Response ($C_V$)')
plt.xlabel('Market Velocity')
plt.ylabel('Reward Multiplier')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot B: Reward Distribution
plt.subplot(1, 2, 2)
plt.stackplot(velocities, sender_share, receiver_share, node_share, 
              labels=['Sender', 'Receiver', 'Node'], alpha=0.8)
plt.title('Tri-Symmetric Reward Scaling')
plt.xlabel('Market Velocity')
plt.ylabel('Units Minted')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

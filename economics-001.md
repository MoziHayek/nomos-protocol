# NEP-001: The Velocity-Based Minting Standard

| Field | Value |
| :--- | :--- |
| **Cybernetic Minting Engine** | Counter-Cyclical Velocity Minting (CCVM) |
| **Mozi Hayek** | Architect |
| **Status** | DRAFT |
| **Type** | Core / Economic |
| **Created** | 2026-02-11 |

## 1. Abstract
This specification defines the algorithmic monetary policy of the Nomos Protocol. Unlike Bitcoin (which mints on a fixed schedule) or Fiat (which mints based on debt), Nomos mints new **UNITT** tokens based on the **Velocity of Money**.

The system functions as a **Cybernetic Thermostat**:
* **State A (Low Velocity):** The protocol increases minting rewards to stimulate commerce.
* **State B (High Velocity):** The protocol decreases minting rewards to prevent inflation.

This ensures the money supply ($M$) expands and contracts dynamically to match the real-time economic output ($Q$) of the network.

## 2. The Core Equation (Theory)
We derive our logic from the Quantity Theory of Money:
$$M \cdot V = P \cdot Q$$

Where:
* $M$: Total Money Supply (UNITT in circulation).
* $V$: Velocity (How often a token changes hands).
* $P$: Price Levels (Inflation).
* $Q$: Real Economic Output (Total Transaction Volume).

**The Nomos Goal:** Keep $P$ stable by adjusting $M$ in response to changes in $V$.

## 3. Protocol Variables

| Variable | Symbol | Definition |
| :--- | :--- | :--- |
| **Target Velocity** | $V_{target}$ | The ideal turnover rate of the currency (e.g., 10.0/year). Governed by the Merit Class. |
| **Current Velocity** | $V_{now}$ | The rolling 24-hour average of `TotalVolume / TotalSupply`. |
| **Base Reward** | $R_{base}$ | The standard minting rate per dollar of commerce (e.g., 0.5%). |
| **Dampening Factor** | $k$ | The sensitivity of the thermostat (prevents oscillation). |

## 4. The Minting Function
For every verified transaction with value $Tx_{val}$, the protocol calculates a Minting Reward ($R_{tx}$).

The Formula:
$$R_{tx} = Tx_{val} \times R_{base} \times \text{Clamp} \left( \frac{V_{target}}{V_{now}} \right)$$

### 4.1. The logic
* **If $V_{now} < V_{target}$ (Economy is Cold):**
    * The ratio $> 1$.
    * The protocol **Boosts** rewards to encourage spending.
    * *Example:* Multiplier becomes $1.5x$. You get paid *more* to trade.
* **If $V_{now} > V_{target}$ (Economy is Overheating):**
    * The ratio $< 1$.
    * The protocol **Cuts** rewards to cool down inflation.
    * *Example:* Multiplier becomes $0.5x$. Minting slows down.

### 4.2. The Clamp (Safety Cap)
To prevent hyperinflation during a total economic freeze (where $V_{now} \to 0$), we apply a hard mathematical clamp:

$$0.1 \leq \frac{V_{target}}{V_{now}} \leq 2.0$$

* **Max Limit:** Rewards can never exceed $2x$ base rate.
* **Min Limit:** Rewards can never fall below $0.1x$ base rate (minting never truly stops, just slows).
### 4.3. The Epoch Identity Ceiling (Daily Human Limit)
To prevent systemic value extraction while permitting infinite transaction velocity, Nomos enforces a time-weighted reward ceiling at the **Identity Layer** rather than the Transaction Layer.

Because every wallet is cryptographically bound to a unique ZK-Nullifier (representing one verified human), the protocol tracks the total rewards minted by each human over a rolling 24-hour epoch.

**The Logic:**
* $\Sigma R_{24h}$: The total UNITT rewards accumulated by a specific ZK-Nullifier in the last 24 hours.
* $C_{daily}$: The maximum protocol subsidy allowed per human per day (e.g., 50 UNITT).

**The Rule:**
* If $\Sigma R_{24h} < C_{daily}$: The transaction mints the standard velocity reward.
* If $\Sigma R_{24h} \geq C_{daily}$: The transaction is processed and settled flawlessly, but it mints **0 UNITT** in rewards. 

**Economic Rationale:**
This removes arbitrary transaction-count limits (e.g., "10 transactions per day") which stifle legitimate economic activity. A user can transact 100 times a day without friction. However, it completely neutralizes "Whale Mining." A high-net-worth individual executing massive trades can still utilize the network, but their ability to extract newly minted supply is strictly capped to the exact same daily limit as every other human in the protocol.

## 5. The 3-Way Split (Distribution)
Once $R_{tx}$ is calculated, it is minted and split immediately via the `VelocityMint.sol` contract:

| Stakeholder | Share | Rationale |
| :--- | :--- | :--- |
| **Buyer** | 33.3% | **Rebate:** Incentivizes spending/velocity. |
| **Merchant** | 33.3% | **Bonus:** Incentivizes accepting UNITT. |
| **Node** | 33.3% | **Fee:** Incentivizes infrastructure/security. |

## 6. Implementation & Finality
To prevent "Wash Trading" (fake velocity), the minted rewards are **not instant**.

1.  **Pending State:** $R_{tx}$ is minted but locked in `EscrowVault`.
2.  **Challenge:** The recipient must provide a **ZK-Liveness Proof** (Proof-of-Humanity) or solve a **UBL Task**.
3.  **Settlement:**
    * If Proof = Valid $\rightarrow$ Funds Unlock.
    * If Proof = Invalid/Timeout $\rightarrow$ Funds Burned.

## 7. Security Considerations
* **Sybil Attacks:** Mitigated by the ZK-Bio requirement for the Rebate/Bonus.
* **Cartel Attacks:** Mitigated by the $V_{target}$ dampener. If a cartel artificially increases $V_{now}$ to print money, the protocol automatically lowers the reward rate for everyone, making the attack unprofitable.

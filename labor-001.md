# NEP-003: The Universal Basic Labor (UBL) Standard

| Field | Value |
| :--- | :--- |
| **Title** | Universal Basic Labor & Proof-of-Verification |
| **Author** | Architect |
| **Status** | DRAFT |
| **Type** | Core / Labor |
| **Created** | 2026-02-12 |

## 1. Abstract
This specification defines the **Universal Basic Labor (UBL)** protocol. Nomos replaces traditional energy-wasteful Proof-of-Work (PoW) and capital-intensive Proof-of-Stake (PoS) with **Proof-of-Verification**. 

UBL is a decentralized micro-task marketplace baked into the protocol layer. It allows any human with a valid ZK-Bio identity to perform cognitive labor that AI cannot reliably perform. 

This serves two primary functions:
1. **The Cold Start:** It allows users with zero capital to earn their first UNITT tokens simply by contributing human attention.
2. **Escrow Unlocking:** It serves as the finality mechanism to unlock pending velocity rewards, proving that a real human was present during a transaction.

## 2. The Labor Pool (Task Types)
The UBL protocol routes specific, verifiable tasks to the Labor Class. These tasks secure the network and enforce the Constitution.

### Type 1: Sybil Defense (The "Nomos CAPTCHA")
* **Purpose:** To prove active human liveness.
* **Task:** The user is presented with a cognitive puzzle (e.g., "Identify the AI-generated anomaly in this audio clip" or "Transcribe this distorted text").
* **Utility:** Protects the network from bot-farming and automated reward draining.

### Type 2: Adjudication & Justice (Article VII)
* **Purpose:** To resolve escrow disputes, chargebacks, or flagged merchant behavior.
* **Task:** The user acts as a "Juror." They are presented with the cryptographic evidence of a disputed transaction and must vote on the outcome based on the Constitution.
* **Utility:** Keeps conflict resolution entirely human-driven, preventing AI Sentinels from executing final judgments (Article VI).

### Type 3: Oracle Verification
* **Purpose:** To bridge real-world data to the blockchain.
* **Task:** Users verify real-world events (e.g., "Did Flight 104 land on time?" or "Is this merchant's physical storefront open?").
* **Utility:** Creates a decentralized, human-powered Oracle network.

## 3. The Consensus Mechanics (How Work is Verified)
To ensure bad actors cannot submit fake work, UBL relies on **Multi-Sig Human Consensus**.



1. **Routing:** A UBL task is encrypted and routed randomly to $N$ independent, ZK-verified humans (e.g., 5 users).
2. **Blind Execution:** The users complete the task without knowing who else is working on it.
3. **Consensus Threshold:** If a supermajority (e.g., 4 out of 5) submit the exact same answer, the protocol accepts the work as valid.
4. **Slashing (Reputation):** The 4 humans who agreed gain Reputation ($Rp$) and UNITT. The 1 human who disagreed (or attempted to cheat) loses Reputation.

## 4. The Reward & Escrow Unlock
UBL is intrinsically tied to the Economic Engine (NEP-001). 

When a transaction occurs, the $R_{final}$ reward is minted into a temporary **Pending Escrow**. To unlock this escrow into liquid UNITT, the user must expend a **Labor Token**.

* **Earning Labor Tokens:** Users earn Labor Tokens by completing UBL tasks. 
* **The Cycle:** 1. User A buys a coffee. (Generates 1 UNITT in Escrow).
  2. User A opens their Nomos App and completes 3 minutes of UBL tasks (e.g., acts as a Juror on a minor dispute).
  3. The UBL smart contract verifies the work and unlocks the 1 UNITT. 

*Note: High-Reputation individuals (Merit Class) can delegate their UBL requirements to lower-tier Labor Class workers, creating a natural internal job market where time-rich users earn UNITT by unlocking the escrow of capital-rich users.*

## 5. TACS Compliance (Zero-Coercion)
The UBL protocol strictly adheres to the Tri-Axiom Compliance Standard:
* **Axiom 1 (Autonomy):** UBL is strictly opt-in. A user who never wishes to perform UBL is not forced to; they simply forfeit their pending minting rewards (or pay a Laborer to do it).
* **Axiom 3 (Impartiality):** The UBL routing algorithm is blind to wealth. A millionaire and a student receive the exact same randomized tasks and are graded on the exact same consensus math.

# NEP-003: The Universal Basic Labor (UBL) Standard

| Field | Value |
| :--- | :--- |
| **UBL-Draft** | The Labor Pools: Blind Routing & Peer-to-Peer Bounties |
| **Mozi.Hayek** | Architect |
| **Status** | DRAFT |
| **Type** | Core / Labor |
| **Created** | 2026-02-13 |

## 1. Abstract
This specification defines the **Universal Basic Labor (UBL)** architecture. In strict adherence to Article I of the Constitution, **no user is ever required to perform UBL**. 

UBL serves as a targeted, recirculatory safety net that allows users with low capital (under the 1,000 UNITT threshold) to earn their way into the economy by performing cognitive labor that AI cannot reliably perform. 

The architecture is split into two distinct systems: The **Protocol Duty Pool** (critical consensus labor) and the **Peer-to-Peer Bounty Board** (non-critical free market labor).

## 2. System 1: The Protocol Duty Pool (Critical Labor)
To prevent cartel gamification and ensure absolute impartiality, critical protocol tasks (Sybil defense, Wash-Trade triage, Constitutional Jury Duty) cannot be manually selected by users.

### 2.1. The Opt-In Mechanism
Users voluntarily toggle their status to "Active" within specific Labor Tiers (Clerical, Oracle, or Adjudication) based on their earned Reputation ($Rp$). They are informed of the standardized compensation rate (funded by the Maturity Clock) prior to joining the pool.

### 2.2. Verifiable Random Function (VRF) Routing
When a protocol-level dispute or flag occurs, the smart contract queries a VRF to randomly and blindly select $N$ active users (e.g., 5 users) from the pool. 
* Users do not know the identities of the other selected workers.
* Users cannot predict which case they will be assigned.

### 2.3. Consensus & Slashing
The $N$ selected users review the evidence and submit a blind vote. If a supermajority agrees, the outcome is finalized. The majority receives the UNITT compensation and $+Rp$. The minority (or those attempting to maliciously vote against clear evidence) receives $0$ UNITT and a heavy $-Rp$ slash. 

## 3. System 2: The Peer-to-Peer Bounty Board (Non-Critical Labor)
For tasks that do not impact the protocol's consensus or security, Nomos provides an open, decentralized job board. 

Any user or merchant can post a specific task (e.g., translation, design, physical delivery) and lock a UNITT bounty in an escrow contract. UBL workers can freely browse this board, evaluate the compensation, and manually pick the tasks they wish to complete.

## 4. TACS & Constitutional Compliance
* **Article I (Voluntary Participation):** Users can ignore VRF drafts without financial penalty (they simply lose their "Active" status in the pool). 
* **Article VII (Justice):** The VRF guarantees that Jurors are independent and cannot self-select into disputes where they hold a conflict of interest.
* **Axiom 3 (Universal Impartiality):** The VRF algorithm is entirely blind to wealth; a millionaire and a student in the UBL pool have the exact same mathematical probability of being drafted for a task.

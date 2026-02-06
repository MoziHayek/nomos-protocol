

### **Nomos Protocol: Engineering-Focused FAQ**

---

#### **1. What is the core design philosophy of Nomos Protocol?**

**Answer:**
Nomos Protocol is designed to create a decentralized economic system where currency issuance is tied directly to verified human activity and transaction velocity. The core principles focus on creating an economy that incentivizes circulation over hoarding, ensures transparency and fairness through human oversight, and self-corrects through algorithmic and human mechanisms to avoid inflation and manipulation.

---

#### **2. How does the reward mechanism work in Nomos Protocol?**

**Answer:**
Nomos uses a 3-way reward split for each verified transaction. When a transaction occurs, rewards are issued as follows:

* **Sender:** Receives 1/3 of the reward for initiating economic flow.
* **Receiver:** Receives 1/3 of the reward for utility creation.
* **Node:** Receives 1/3 of the reward for validating the transaction and maintaining infrastructure.

This reward system aligns the interests of all participants and encourages economic movement rather than passive accumulation.

---

#### **3. Can you explain the “Decimal Scarcity Algorithm” and how it prevents inflation?**

**Answer:**
The **Decimal Scarcity Algorithm** ensures that as the network grows, the reward distribution becomes increasingly scarce to prevent runaway inflation. It is calculated based on transaction volume and circulating supply. The scarcity factor is controlled by:

* **X = total transaction volume** (last 30 days),
* **Y = circulating supply**,
* **N = number of decimal digits in (X + Y)**.

This results in a scarcity factor (**r_s**) that decays logarithmically, not abruptly, allowing the system to adjust gradually to increased usage. The goal is to prevent hyperinflation while maintaining incentivization for network participation.

---

#### **4. How does the **Elastic Velocity Stimulus** work?**

**Answer:**
The **Elastic Velocity Stimulus** controls the minting of new tokens based on the speed at which the network is transacting. The system has a target velocity (**V_T**) which is the desired amount of transaction volume per month, and the actual velocity (**V_A**) is calculated from the real transaction volume.

The **Velocity Coefficient** (**C_V**) adjusts the reward issuance:

* **C_V = V_T / max(V_A, ε)**, where ε is a small value to prevent division by zero.

This coefficient is clamped between **0.5** and **2.0**, ensuring that rewards are neither too high nor too low, preventing both runaway minting and stagnation.

---

#### **5. What is the minting formula for rewards?**

**Answer:**
The formula for minting rewards (**R**) is:

* **R = V × r_s × C_V**, where:

  * **V** = transaction value,
  * **r_s** = scarcity factor from the Decimal Scarcity Algorithm,
  * **C_V** = velocity coefficient from the Elastic Velocity Stimulus.

This formula ensures rewards are proportional to the value being transacted, adjusted for scarcity and economic velocity.

---

#### **6. What is the role of **Nodes** in the Nomos Protocol?**

**Answer:**
Nodes play a crucial role in the validation and infrastructure of the Nomos Protocol. They are responsible for:

* Validating transactions to ensure they comply with protocol rules.
* Ensuring the integrity of the network by checking that transactions are legitimate and not part of any manipulation.
* Collecting rewards for their validation work and contributing to the overall infrastructure.

Additionally, nodes can allocate a percentage of their rewards to public goods, such as **UBL pools** or **reliability pools**, which contribute to the protocol’s long-term stability.

---

#### **7. How does the **Anti-Manipulation Layer** work?**

**Answer:**
The **Anti-Manipulation Layer** uses the **Nomos Sentinel**, an AI-driven pattern recognition system, to flag suspicious activities, such as synthetic or non-human behaviors. When a transaction is flagged, the mint rewards associated with that transaction are placed into **Protocol Escrow**. This layer performs several functions:

* **Dampens inflationary reflex loops** by delaying reward minting.
* **Neutralizes reward-farming incentives** by removing immediate ROI.
* **Protects against irreversible economic harm** from automated systems.

Once flagged, the user is given options to resolve the issue through one of the **Resolution Pathways**, which include AI-assisted mitigation or human review by the **Nomos Jury**.

---

#### **8. What are **Resolution Pathways** and how do they work?**

**Answer:**
Resolution Pathways are the steps users can take if their transaction is flagged by the **Nomos Sentinel**. Users have several options, including:

* **Voluntary Forfeiture**: The user acknowledges the issue, and rewards are routed to a public goods pool.
* **AI-Assisted Mitigation**: The system evaluates historical behavior and releases or reclaims rewards based on intent.
* **Human/Jury Review**: If the issue persists, a group of human jurors evaluates the situation and decides on the outcome, which can include temporary suspensions or reputation penalties.

These pathways ensure transparency and fairness in how flagged transactions are handled, with the goal of providing **due process** to users.

---

#### **9. How is **Governance** handled within Nomos Protocol?**

**Answer:**
Governance within **Nomos** is a **reputation-weighted** system, where users with higher reputation scores can influence decision-making. Some key points about governance include:

* **Reputation-Weighted Voting**: Users can vote on protocol changes, and the weight of their vote depends on their reputation.
* **Constitutional Constraints**: The **Nomos Constitution** guarantees that certain rights, such as voluntary participation and property sovereignty, are immutable and cannot be overridden by governance decisions.
* **Jury System**: A **Nomos Jury** handles disputes and ensures that economic penalties or rewards are fairly distributed.

Governance decisions require a quorum, majority vote, and a time-lock, ensuring that decisions are made transparently and with adequate consideration.

---

#### **10. What is **UBL (Universal Basic Labor)** and how does it function within the protocol?**

**Answer:**
**Universal Basic Labor (UBL)** is a mechanism that allows participants, especially those with limited resources, to engage in meaningful economic activities to earn rewards. The process works as follows:

* **Donors** fund proof-of-human tasks that can be verified on-chain.
* **Participants** complete the tasks, which are designed to be useful and beneficial to the protocol or the broader ecosystem.
* **Rewards** are minted as a result of these activities, which encourages active participation.

UBL tasks are designed to be **non-extractive**, meaning they contribute to the protocol’s value in a way that benefits the entire ecosystem, ensuring fairness and integrity.

---

#### **11. How do you ensure the **Scalability** of the system?**

**Answer:**
Nomos Protocol uses several mechanisms to ensure scalability, including:

* **ZK-Sharding**: Zero-knowledge sharded data storage improves scalability by splitting the data into smaller chunks that can be processed in parallel.
* **Tiered Node Scaling**: The network is designed to accommodate primary nodes (core validators) and edge nodes (opt-in devices that provide compute/storage), distributing workload efficiently.
* **Randomized Uptime Challenges**: Nodes are incentivized to stay online and maintain the network's integrity through uptime challenges and reliability bonuses.

These mechanisms work together to ensure that the protocol can scale as the number of users and transactions grows.

---

### **Conclusion**

This engineering FAQ provides a comprehensive overview of the **Nomos Protocol** for developers and technical users, clarifying how the system functions, how rewards are issued, and how various mechanisms contribute to the protocol's stability, security, and fairness. By addressing the key technical details, this FAQ can serve as an accessible guide for those looking to engage more deeply with the protocol or contribute to its development.

---


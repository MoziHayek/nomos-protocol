# Nomos — Finalization, Evidence Persistence, and Reward Distribution (v0 amendment)
Author: @MoziHayek  
Purpose: amend the engineering spec to (1) require canonical persistent evidence storage (Codex / NomosDA), (2) reconcile whitepaper reward split (1/3 Sender / 1/3 Receiver / 1/3 Node) with attester/juror incentives, and (3) define a bifurcated finalization (Settlement + Issuance/Escrow) flow so base transfers are immediate while issuance rewards are escrowed pending Sentinel/Jury resolution.

Status: implementer-facing. Replace or add this file under `spec/` and link from `spec/engineering-spec.md` and the attestation/reputation & dynamic-velocity specs.

---

## 1. Goals and rationale
- Evidence persistence: evidence used in disputes must remain available even if the originating Sentinel/Node goes offline during long jury processes. Nomos uses Codex or NomosDA as canonical evidence stores (with IPFS as optional fallback). All evidence URIs in the system MUST reference an immutable Codex/NomosDA locator (or a signed mirror) to guarantee retrieval and auditability.
- Whitepaper reward mandate: maintain the whitepaper's 1/3 split of minted UNITT between Sender, Receiver, and Node as a canonical distribution rule for any IssuanceEvent.
- Node pool distribution: the "Node" third is a Node Pool that funds operating nodes, attesters, jurors, Sentinel services, and any protocol infrastructure. Attester and juror payments are drawn from the Node Pool (or explicitly from protocol reserve if desired).
- Bifurcated finalization: separate Settlement (immediate transfer/confirmation of the base economic value being moved) from Issuance (newly minted UNITT rewards). Only the latter is subject to dispute escrow.

---

## 2. Evidence persistence / evidence_uri policy

Canonical evidence descriptor (new typed field)
- All places that previously used `evidence_uri` or `rationale_uri` MUST include an `evidence_locator` object with canonical store metadata and a fallback chain.

EvidenceLocator (JSON)
```json
{
  "store": "codex|nomosda|ipfs|http",
  "locator": "codex://<collection>/<cid>|nomosda://<id>|ipfs://<cid>|https://...",
  "signed_manifest": "ipfs://<cid-of-signed-manifest>",
  "stored_at": 1690000000,
  "persistence_proof": { "tx_hash": "...", "anchor": "chain:tx" },
  "uploader": "addr_or_pubkey"
}
```

Requirements
- Prefer `store` = `codex` or `nomosda`. If a Sentinel or other node produces evidence, it MUST push evidence to Codex/NomosDA and include the resulting `locator`.
- `signed_manifest` is recommended: a signed manifest (by the producing node/service) containing input hashes, feature vectors (for Sentinel) and a canonical reference so jurors can reproduce the model input.
- If Codex/NomosDA is temporarily unavailable, nodes may include a signed `ipfs://` fallback, but the canonical evidence must be migrated/anchored to Codex/NomosDA within a configured migration window (e.g., 7 days) or the alert is considered weaker evidence (affects confidence).
- The engine must validate that `evidence_locator` resolves to stored content with matching hashes before accepting an attestation/challenge relying on it.

APIs
- Registry & evidence endpoints:
  - POST /evidence — uploader pushes & receives `evidence_locator` (service/agent authenticated)
  - GET /evidence/{locator} — resolver to fetch metadata/status (replication status, anchors)
  - GET /evidence/{locator}/verify — returns content hashes and anchored proof

Auditability
- For every SentinelAlert, Attestation, Challenge, and JuryVote that references evidence, store the EvidenceLocator alongside the respective record. Juries and auditors should prefer evidence where `store` is `codex` or `nomosda`.

---

## 3. Reward distribution model (whitepaper alignment)

Canonical mint split (must be used by IssuanceEngine)
- For every mint_amount M produced by the Issuance Engine, the canonical distribution is:
  - Sender share = M * 1/3
  - Receiver share = M * 1/3
  - Node pool = M * 1/3

Definitions
- Sender: the account initiating the underlying base transaction or economic action.
- Receiver: the intended recipient of the base economic measure (the primary beneficiary/claimer).
- Node pool: a protocol-managed pool representing node operators, attesters, jurors, and other infrastructure participants.

Node Pool distribution rules (v0 recommended)
- The Node Pool is not simply left intact; at settlement/finalize time a portion is distributed to participating attesters & jurors for the specific claim as follows:
  - Claim-specific distribution: X% of Node Pool share is allocated immediately to attesters & jurors who participated in validating that claim (pro-rata by their recorded contribution weights).
  - Remainder (Node Maintenance Reserve): the leftover remains in the Node Pool for node operators and protocol maintenance.
- Example split parameterization (governance-configured):
  - node_claim_distribution_pct = 0.60  // 60% of node_share used to reward attesters/jurors on this claim
  - node_reserve_pct = 0.40              // 40% retained in Node Pool
- Within the claim-specific distribution:
  - attester_rewards_pct = 0.65  // 65% of claim-specific distribution to attesters (divided by effective_weight)
  - juror_rewards_pct = 0.35     // 35% to jurors (divided equally or weighted if governance chooses so)
- These percentages are parameters and must be configurable via governance; defaults above keep attesters as major claim verifiers while honoring juror incentives.

Rationale
- This preserves the 1/3 whitepaper split while pragmatically compensating attesters/jurors from Node Pool rather than changing the whitepaper's Sender/Receiver/Node equality.

Edge cases & governance
- If a claim has no attesters or jurors (unlikely), the system moves the node-specific claim distribution into Node Pool reserve for later disbursement.
- All distribution computations are recorded in IssuanceEvent and EscrowRecord for transparency.

---

## 4. Bifurcated finalization (settlement + issuance/escrow)

Concept
- Settlement (Phase 1) — immediate confirmation/transfer of the base economic value (the underlying amount_econ_measure). This must not be blocked by Sentinel or jury activity.
- Issuance (Phase 2) — minting of UNITT rewards computed from the claim. Mint_amount may be immediately minted if not flagged, or minted into an ESCROW state and held until cleared by sentinel/jury flow.

New artifacts & schema additions

SettlementEvent
```json
{
  "settlement_id": "uuid",
  "claim_id": "uuid",
  "amount_settled": 123.45,
  "currency": "USD",
  "sender": "addr",
  "receiver": "addr",
  "settlement_tx": "onchain-tx-hash-or-null",
  "timestamp": 1690000000,
  "status": "confirmed|failed",
  "notes_uri": "evidence_locator or null"
}
```

EscrowRecord (for issuance)
```json
{
  "escrow_id": "uuid",
  "issuance_id": "uuid",
  "claim_id": "uuid",
  "mint_amount": 1000,
  "sender_share": 333.333,
  "receiver_share": 333.333,
  "node_pool_share": 333.334,
  "node_claim_distribution": {
    "to_attesters": 200,
    "to_jurors": 100,
    "to_reserve": 33.334
  },
  "escrow_state": "held|released|slashed|partially_released",
  "hold_reasons": ["flagged_by_sentinel","challenged","appeal_pending"],
  "escrowed_at": 1690000100,
  "release_conditions": {
    "condition_type": "clear_by_jury|timeout|governance_override",
    "condition_params": { "timeout_seconds": 604800 }
  },
  "release_tx_hash": null,
  "notes_uri": "ipfs://... or evidence_locator"
}
```

IssuanceEvent (amended)
- Add fields:
  - `settlement_id` — link to SettlementEvent
  - `escrow_id` — link to EscrowRecord (if escrowed)
  - `velocity_multiplier` — multiplier applied at finalize
  - `final_mint_status` — `minted_onchain|minted_escrowed|reverted|not_minted`
  - `distribution_details` — computed splits and per-party amounts
  - `evidence_locators` — array of EvidenceLocator objects used in final decision

---

## 5. Sequence flows (concise)

Happy path — unflagged issuance (no escrow)
1. Claim submitted.
2. Settlement (Phase 1):
   - Engine triggers or verifies base transfer: POST /claims/{id}/settle (or verify on-chain).
   - SettlementEvent recorded with `settlement_tx`.
3. Attestations satisfy threshold; no Sentinel flag or challenges occur during T_open.
4. Finalize issuance:
   - IssuanceEngine computes mint_amount (M') (applies VelocityMultiplier).
   - Mint occurs onchain or via programmatic mint (Finalization Phase 2) and IssuanceEvent records distribution (Sender, Receiver, Node Pool). No escrow created.

Flagged/challenged path — escrowed issuance
1. Claim submitted.
2. Settlement (Phase 1) completes immediately; SettlementEvent recorded.
3. Attestation(s) occur but Sentinel issues alert or a challenge is filed.
4. IssuanceEngine computes mint_amount M' but creates EscrowRecord and mints Node/Sender/Receiver shares into escrow (or records mint intent with `final_mint_status = minted_escrowed`).
   - Practical implementation: either mint tokens to a protocol-managed escrow contract or keep mint pending — recommended: mint into escrow contract to guarantee availability for release.
5. Jury flow resolves claim:
   - If Accepted: EscrowRecord transitions to `released` and tokens are transferred to Sender/Receiver/Node-pool-distribution per computed splits; Node-pool sub-distributions to attesters/jurors processed.
   - If Rejected: EscrowRecord transitions to `slashed` per slashing rules; slashed tokens go to winner(s) + protocol reserve as configured.
6. Release/Slash recorded with release_tx_hash and IssuanceEvent updated.

Notes on minting vs escrow strategy
- Two approaches:
  - Pre-mint-to-escrow: mint tokens at finalize time into a protocol escrow contract. Guarantees tokens exist, simplest for short windows.
  - Mint-on-release: do not mint until claim cleared (tokens not created until acceptance). Safer fiscally but requires reliable treatment to prevent double issues if delay causes state divergence.
- Recommendation: use pre-mint-to-escrow for v0 with strict governance caps and protocol_reserve funding to back escrow obligations; ensure escrow is controlled by multisig and/or governed release contracts.

---

## 6. API additions & governance controls

New endpoints (examples)
- POST /claims/{claim_id}/settle
  - Idempotent endpoint to register/confirm the base economic transfer and create SettlementEvent. Must be called by settlement operator or verified by on-chain proof.
- POST /claims/{claim_id}/create_escrow
  - Creates EscrowRecord and (optionally) mints tokens to Escrow contract. Only called when issuance is pending and policy requires escrow (flagged or challenged).
- POST /escrows/{escrow_id}/release
  - Release escrowed tokens per computed distribution. Only callable by engine after condition satisfied (jury accepted, or timeout+governance).
- POST /escrows/{escrow_id}/slash
  - Slash escrow per outcome. Requires governance policy checks; recorded and auditable.

Governance controls
- Parameters:
  - escrow_mint_strategy: pre_mint | mint_on_release
  - escrow_timeout_seconds: default 7 days (if no resolution, governance path to process)
  - escrow_release_quorum: e.g., jury accepted or governance multisig if jury fails
  - max_escrow_amount_per_period: prevents runaway minting into escrow
- Emergency actions:
  - governance multisig can force release or force revert an escrow; all actions recorded with rationale_uri.

---

## 7. Edge cases & operational notes

Atomicity & user UX
- Settlement must not be blocked by escrow. Users expect base value transfer confirmation quickly.
- Escrow status must be clearly visible: client SDKs and UI should show the base transfer confirmed and the issuance rewards `escrowed` with expected release conditions.

Dispute timeouts
- For long-running disputes, EscrowRecord.release_conditions should include a `timeout_seconds`. If timeout elapses without final jury decision, escrow goes to governance resolution via multisig vote.

Evidence continuity
- If a sentinel node that produced evidence goes offline, archival of that evidence in Codex/NomosDA prevents evidence loss. If evidence is only in ephemeral local storage, the case weakens; rules should favor evidence with a `persistence_proof` pointing to Codex/NomosDA.

Accounting & treasury
- Node Pool mechanics must be transparent; all Node Pool inflows/outflows are recorded on-chain or in auditable storage.
- If pre-mint-to-escrow is used, treasury must ensure initial backing and accounting.

Performance & cost considerations
- Using Codex/NomosDA for all evidence increases storage & anchoring costs. Balance requirements by allowing succinct signed manifests + off-chain archives for large artifacts; require critical evidence (rationale, hashes, signatures, features) to be stored in Codex/NomosDA.

---

## 8. Acceptance criteria for this amendment
- Attestation, SentinelAlert, and Challenge records accept `EvidenceLocator` objects and engine validates them against Codex/NomosDA resolvers.
- SettlementEvent and EscrowRecord are implemented and linked in the claim lifecycle.
- IssuanceEvent contains settlement_id, escrow_id (if applicable), final_mint_status, and distribution_details.
- Escrow transitions (held → released/slashed) are recorded immutably with release_tx_hash and rationale_uri.
- Node Pool distribution rules enforce the whitepaper 1/3 Sender / 1/3 Receiver / 1/3 Node split; claim-level node distributions to attesters/jurors are computed from Node Pool share according to node_claim_distribution parameters and recorded in EscrowRecord and IssuanceEvent.
- SDK / UI shows: Settlement confirmed; Issuance: escrowed (if flagged) + expected release conditions; audit endpoints expose evidence locators and anchored proofs.

---

## 9. Implementation checklist (concrete steps)
1. Add `spec/finalization-evidence-and-rewards.md` to repo and link from main spec README.
2. Update JSON schemas in `spec/engineering-spec.md`, `spec/attestation-and-reputation.md`, and `spec/dynamic-velocity-and-sentinel.md` to include `EvidenceLocator`, SettlementEvent, EscrowRecord, and amended IssuanceEvent fields.
3. Implement /evidence endpoints and Codex/NomosDA resolver integration in reference engine (or provide a shim that validates locators and checks anchoring).
4. Implement Settlement endpoint and ensure settlement is immediate and idempotent.
5. Implement Escrow creation/release/slash logic and an escrow contract (if pre-mintable) with multisig governance hooks.
6. Update simulator to model pre-mint-to-escrow vs mint-on-release and measure treasury exposure.
7. Update SDK and UI to present bifurcated finalization state clearly.

---
# Candidate object: harmonic branch-deletion obstruction

**Candidate claim.** `CA-HARMONIC-BRANCH-DELETION-OBSTRUCTION-v1`  
**Draft status.** Source-read, independently replayed, retained in this Boss6 delegate workspace; no `clean done` was issued and no formal archive object was overwritten.  
**Frozen source IDs.** `9ead0718e1f922fb0462` (JSON certificate), `b81e4d0d48f6fad07a88` (explanation), and `f3001ca6d7e2a9123d95` (verifier).  
**Source SHA-256.** JSON `6205c92730b8fdebb012b0562d3bca6f640dfca75e81c305a8daa3f263aad541`; Markdown `db9d7f6ebb2acbc8f80e5c10a77c9e102cb9b47665d0117b2c421ef129baa3d7`; verifier `5055f6dbc9f582231f23279213b8e9e1004fa53a408f3453e8002372643a7779`.

## Mathematical statement

For a terminal ordered profile $z$, let $c_x(z)$ be the number of selected themes that cover customer $x$, and let $H_k=\sum_{j=1}^k1/j$.

\[
\Phi(z)=\sum_x H_{c_x(z)}.
\]

If $z^{-i}$ is obtained by deleting player $i$'s selected theme (the other selected themes stay in place), then the allocated payoff is exactly

\[
u_i(z)=\Phi(z)-\Phi(z^{-i}).
\]

At any complete-history SPE node $h$, the action $A^*$ prescribed by the strategy and a forced action $A$ satisfy

\[
\Phi(z_{A^*})-\Phi(\bar z_{A^*})
\geq
\Phi(z_A)-\Phi(\bar z_A),
\qquad \bar z=z^{-i}.
\]

Rearranging leaves the branch-dependent deletion gap

\[
\Phi(z_{A^*})-\Phi(z_A)
\geq
\Phi(\bar z_{A^*})-\Phi(\bar z_A),
\]

whose sign is not controlled by SPE. Therefore SPE does not imply that the prescribed continuation maximizes terminal harmonic potential among the current actions.

## Exact finite witness

The common catalog has six themes

\[
T_0=\{1,2\},\ T_1=\{2\},\ T_2=\{1,3\},\ T_3=\{0,1\},\ T_4=\{0,3\},\ T_5=\{3\},
\]

and four unit customers with interest signatures

\[
\{T_0,T_1\},\quad \{T_0,T_2,T_3\},\quad
\{T_2,T_4,T_5\},\quad \{T_3,T_4\}.
\]

There are three ordered players.  The JSON records an action at the root, at all six one-action histories, and at all 36 two-action histories (43 history nodes total).  A complete exact check covers 215 unilateral deviations.  One SPE path is

\[
(T_1,T_3,T_4),
\]

while forcing $T_0$ at the root and then following the same certificate gives

\[
(T_0,T_0,T_4).
\]

The root payoff is $1$ on both branches, so the root deviation is an SPE tie.  The topic-count vectors are respectively

\[
(0,1,0,1,1,0)\quad\text{and}\quad(2,0,0,0,1,0).
\]

The induced customer-load multisets are $(2,1,1,1)$ and $(2,2,1,1)$ (the order of customer labels is immaterial).  Hence

\[
\Phi_{\mathrm{actual}}=H_2+3=\frac92,
\quad
\Phi_{T_0}=2H_2+2=5,
\]

and the actual branch has lower potential by $-1/2$.  Deleting the root player gives potentials $7/2$ and $4$, so the deletion gap in the SPE comparison is also $-1/2$.  Both branches have welfare $W=4$, and exact enumeration gives $\mathrm{OPT}_3=4$.

This is a finite, fully checked obstruction to the inference

\[
\text{full-history SPE} \Longrightarrow
\text{branchwise harmonic-potential maximization}.
\]

It is not a Q-CAG-HALF counterexample, not a welfare gap, and not evidence that any alternative potential or cross-history payment scheme is impossible.

## Independent replay

The frozen verifier was copied byte-for-byte to `audit/runtime/a/b/c/d/e/verify.py`; the frozen JSON was placed beside it.  The runtime imports the `customer_attraction` implementation from the frozen `main` commit `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`.  Running

```sh
python3 cleanup/workspaces/Boss6/delegates/potential_obstruction/audit/runtime/a/b/c/d/e/verify.py
```

returned `status=passed`, `histories=43`, `deviations=215`, `actual_history=[1,3,4]`, `forced_root_history=[0,0,4]`, `phi_actual=9/2`, `phi_forced=5`, `phi_deleted_actual=7/2`, `phi_deleted_forced=4`, `potential_gap=-1/2`, `deletion_gap=-1/2`, `welfare=4`, and `optimum=4`.  The verifier uses exact `Fraction` arithmetic and `verify_certificate`; no floating-point acceptance is involved.

The exact source copies are in `source/`, and the replay output is `audit/verifier-output.json`.  The runtime package is only a replay dependency; it is not being claimed as a new mathematical source.

## Comparison with existing objects and corrections

| Related object | Relationship and boundary |
|---|---|
| `customer-attraction/full-tree-averaging-obstruction` | Gives the general fixed-$\sigma$, fixed-$q$ Farkas interface and the exact iid-prefix identities with deletion-position terms.  Its later correction restricts the Farkas statement to the fixed policy/distribution cone; it does not assert a universal certificate.  The present witness is narrower and pointwise: it shows one SPE branch comparison has a signed deletion gap.  It does not refute the full per-history, per-deviation certificate form. |
| `customer-attraction/iid-static-security-benchmark` | Proves that static symmetric mixed Nash distributions maximize expected harmonic potential and gives $nv_n\le Z_n\le\mathrm{OPT}_n$.  It is a simultaneous-play benchmark and explicitly does not give sequential SPE payment $W\ge Z_n$; the present root tie is a sequential branch obstruction, not a contradiction of the static theorem. |
| `customer-attraction/six-theme-three-player-conditional-iid-payment` | A positive 63-column certificate for one fixed six-theme, three-player policy and uniform $q$, valid on its specified SPE/static-Nash customer cone.  That conditional theorem and this witness are compatible: a welfare certificate on a fixed cone does not make every SPE branch a harmonic-potential maximum.  Neither quantifies all policies, $q$, or six providers. |
| `customer-attraction/boolean-harmonic-potential-inversion` | Gives a unique (possibly signed) customer-type representation for a prescribed Boolean subset potential.  It also warns that for an ordered deviation the comparison is between two potential differences with different continuations, not between terminal potentials alone.  This supports the identity used here but does not supply branch monotonicity or legal nonnegative weights for arbitrary count states. |
| `CA-R086-HARMONIC-FUTURE-RESPONSE-OBSTRUCTION-20261030` (`调和势链未来回应项--障碍.md`) | Independent four-theme/three-player, 21-history/84-comparison witness.  It records zero source/replay IC regret with a positive future-response term and $W=\mathrm{OPT}_3$.  It rules out paying a specific reset route from the same IC slacks; it does not rule out other potentials or prove a target counterexample.  The current witness isolates the simpler branchwise $-1/2$ potential/deletion gap. |
| `customer-attraction/last-two-individual-floor-and-all-n-welfare` | General proved bound $W\ge 4(n-1)\mathrm{OPT}_n/[n(2n-1)]$, giving $8/15$ at $n=3$.  It uses single-step marginal identities and explicitly does not assume SPE is a potential extremum.  The present $W=\mathrm{OPT}_3$ example is consistent with that theorem. |
| `customer-attraction/terminal-reply-conditional-dual-lift` | Conditional end-reply normalization transports a specified dual certificate while exposing incumbent/deletion transfer terms and a DAG.  It explicitly leaves the universal input-certificate obligation open.  The present negative gap is evidence that the transfer remainder cannot be silently dropped. |
| `customer-attraction/independent-individual-and-flow-auditor-contracts` | Separately audits a 34-customer six-theme policy and the full-tree flow identities.  Its 34-customer policy and welfare values are not this four-customer certificate; its flow/template boundaries agree with the present replay and must not be merged into one witness. |
| `CA-CROSS-BRANCH-RELAY-v1/v2` (governance ledger) | A later correction changed the generic claim from the false ΔW≤ΔV to ΔW=ΔV+ΔP−Γ; only the root has (P=0).  This keeps non-root player-profit changes separate from deletion-potential bookkeeping.  The current witness is a root comparison and does not revive the false non-root statement. |
| `CA-STATIC-SMOOTHNESS-SPE-BRIDGE-NO-v1` (governance ledger) | Static smoothness/PNE inequalities do not automatically transfer to sequential full-history SPE.  This is a neighboring bridge obstruction, not an alternative interpretation of the present harmonic identity. |
| Boss5 `dynamic_iid_resume/comparison_cleanup_failure_audit.md` | Later cleanup explicitly lists this four-customer witness as “$W=\mathrm{OPT}_3$, potential branch difference $-1/2$” and warns that it only rejects the written potential/template route.  It does not promote it to a half-coverage negative result. |

The current repository therefore has a consistent correction chain: preserve the exact static potential identity; preserve deletion and future-response terms with their signs; distinguish fixed-policy conditional certificates from universal claims; and keep all finite witnesses outside the six-provider half-coverage conclusion unless their welfare ratio actually fails.

## Exact scope and next use

**Established:** the displayed finite common-catalog certificate is a full pure SPE on all ordered histories; the harmonic utility identity is exact; the prescribed branch can have strictly lower terminal potential than a tied root deviation; and both potential gaps are exactly $-1/2$.

**Not established:** a counterexample to Q-CAG-HALF, failure of all harmonic or non-harmonic proofs, failure of the full per-deviation Farkas interface, or any universal statement for arbitrary (m,n).

Any future harmonic-potential proof must either make the signed deletion gaps telescope/pay them with additional cross-history structure, or use a state variable that controls them.  A line that simply replaces the SPE payoff comparison by “$\Phi$ is nondecreasing under every current action” is invalid on this exact witness.


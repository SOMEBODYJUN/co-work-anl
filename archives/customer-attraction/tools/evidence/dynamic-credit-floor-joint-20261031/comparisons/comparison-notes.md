# Dynamic-credit floor/joint probe comparison notes

## Source and replay table

| ID | Source | Size / SHA-256 | Execution | Archive disposition |
|---|---|---:|---|---|
| `674ba981020cd43dd144` | `dynamic_credit/floor_cone_diagnostic.py` | 2697 B / `efb51e99fa5f2519687f23ba0284dd8a980980ce303aa2fb5c7abb20ed21211e` | Direct root run failed at import because `customer_attraction` was absent; a read-only reconstruction using the frozen exact-spe package, strategy-cone audit module, and archived `residual_counterexample.json` completed 2 target LPs and printed `no positive 2 1.1102230246251565e-16 ...`. | integrated finite diagnostic |
| `d33998326f4e4a417569` | `dynamic_credit/joint_one_step_probe.py` | 1581 B / `626b875306ffb916b30e3c55902f447a64eff4bf10e8673f46305793e6c513b4` | Deterministic direct replay with seed 942; trial 9 found gap `1/7`, the six nonzero mask weights, and `minrow 0`. | integrated finite probe |

Original source bytes are frozen under `original/`. Replay stdout, the direct import failure, and exit code are under `replay/`. The source inventory blobs are `7fab0cf3fb3e74b709cf82951a74bd06c60e6007` and `d31614620e56358c844d10a038d70d8664fe55ae` respectively.

## Mathematical roles

### 1. Individual floor-cone diagnostic (`674ba...`)

`floor_cone_diagnostic.py` searches a fixed full-SPE strategy cone. It loads each parsable archived example with `Instance.from_dict`, restricts to (k\le6,m\le4), obtains two lowest welfare targets from `ExactSPESolver`, and turns each target certificate into `StrategyCone`. The cone rows encode every ordered-history deviation for that fixed action table. For each used target topic and each support of size `min(k,m)`, it maximizes

\[
  c_S(T)-(2m-1)u_t(T)
\]

under nonnegative customer mass, all cone inequalities, and welfare normalization (w_{\rm welfare}=1). Positive floating values would be rationally recovered, converted to integer clones, independently checked, and passed to `verify_certificate`.

The replayed local examples produced only two target LPs and no positive value; the best floating value was (1.11\times10^{-16}), numerically zero. This is weaker than a universal no-witness result because the original worktree's complete example directory was not part of the exported source. It is also distinct from the older fixed-policy floor probe, whose hard-coded (m=3,k=6) run reported a negative best score.

### 2. Joint one-step probe (`d339...`)

`joint_one_step_probe.py` fixes (r=3,k=4), enumerates nonempty masks, samples 3000 response maps with seed 942, and builds one LP combining root utility differences, two-times-tail-profit rows, and coverage/profit rows. The equality fixes actual-path coverage mass to one. The target compares coverage on topics `(1,2,3)` against twice the actual path `(0, response[0])`.

Replay gives:

- trial `9` response map `{0:(2,2), 1:(1,2), 2:(2,3), 3:(2,3)}`;
- gap `1/7`;
- nonzero weights `w_2=9/14`, `w_3=1/14`, `w_4=1/2`, `w_5=3/14`, `w_8=1/2`, `w_9=3/14`;
- `minrow=0`, so no strict margin.

This is a finite floating LP witness for the written projection rows. It has no full strategy tree, no off-path SPE continuation, no exact certificate, and no all-response-map quantifier.

## Comparison to existing dynamic-credit objects

| Existing object | What it certifies | Relation to this batch |
|---|---|---|
| `动态信用固定策略floor LP探针--计算.md` | One hard-coded (m=3,k=6) strategy and finite floating floor score; best violation was negative. | Same broad floor motivation, but current floor source enumerates certificates from exact solver and tries integer-clone recovery; no positive witness in the exported local examples. |
| `动态信用一步闭合随机LP探针--计算.md` | Root utility and two-times-tail-profit rows; trial 2 gap (1/16). | Same (r=3,k=4) random-map style, but current joint source adds coverage/profit rows; gaps are not additive or interchangeable. |
| `动态信用一步覆盖LP探针--计算.md` | Coverage equality and coverage-oriented rows; trial 9 gap (1/5). | Current joint source combines coverage with root/profit constraints and obtains (1/7); it is a separate LP. |
| `动态信用一步闭合标量反例--反例.md` | Exact finite scalar projection (W=14,\u200bOPT=30,\u200b2W-OPT=-2), explicitly `not an SPE`. | Stronger exact arithmetic but known terminal deviation; current probe has no full SPE check and cannot repair that gap. |
| `动态信用一步闭合标量投影障碍--障碍.md` | Why two scalar summaries do not close arbitrary induction; exact terminal best-response failure. | Current joint rows are a larger finite projection, not a proof that the obstruction disappears. |
| `动态信用末位利润余项Fraction审计--计算.md` and background remainder lemma | Exact terminal/background accounting and open early-credit boundary. | Supplies comparison semantics only; does not turn a one-step floating LP into a global welfare proof. |
| `分数覆盖的真实前缀利润预算--引理.md` | Proven prefix payment inequality and (F_m(\tau)) product bound under complete SPE. | Different certificate: a real-path budget argument, not a random local projection. |

## Disposition and non-upgrades

Both sources are integrated as finite customer-attraction computation objects. The floor source's “no positive” replay is recorded with its dependency and input limitation; it does not establish a universal floor. The joint source's `1/7` is recorded with exact recovered weights but remains a floating LP discovery; `minrow=0` rules out claiming a strict robust margin. Neither source supplies a complete strategy, a full SPE certificate, a Q-CAG-HALF theorem/refutation, or an unrelated-machines result. No numerical gap is promoted to a general theorem, and no source is treated as a duplicate of the exact scalar obstruction.

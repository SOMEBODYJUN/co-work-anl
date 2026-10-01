# Running the research algorithms

Choose the solver by its mathematical preconditions. [ASSETS.md](ASSETS.md) gives the proof, implementation, test and certificate path for each claim; [CLAIMS.md](CLAIMS.md) records the exact quantifiers. Run these commands from the repository root with Python 3.

| Question | Applicable conditions | Command | Meaning of output |
| --- | --- | --- | --- |
| Universal shared-catalog bound | Both facilities have the same nonempty legal site set; positive rational weights; linear realized-load customer cost; independent mixed exact customer NE | `python3 -m facility_spe.shared_phi examples/shared/tiny.json` | Constructed factor at most phi, not instance optimal |
| Universal heterogeneous-catalog bound | Two nonempty legal site sets, possibly different; same weight, cost and customer rules; pure exact customer NE | `python3 -m facility_spe.heterogeneous_two examples/heterogeneous/tight_two_M1000.json` | Constructed factor at most 2, not instance optimal |
| Instance-optimal factor | Same linear two-facility game; exponential time in maximum cross-pair overlap is acceptable | `python3 -m facility_spe.exact.bounded_overlap examples/heterogeneous/tight_two_M1000.json` | Exact instance optimum by support-cell enumeration; its certificate verifies attainment |
| Instance-optimal factor, one common customer per pair | Every legal cross pair has at most one common customer | `python3 -m facility_spe.exact.single_overlap examples/heterogeneous/rho_lower.json` | Exact instance optimum in the restricted input class |

All sites list customer IDs under `locations`; IDs start at zero. Heterogeneous and exact solvers require `U1` and `U2`, each a nonempty list of legal sites. Every covered customer must participate; uncovered customers have no payoff. The model has no distance, opening cost, capacity limit, or third facility. Use exact rational or decimal strings or JSON integers for weights. The command-line readers preserve JSON decimals exactly.

Example heterogeneous input:

```json
{
  "weights": ["1/3", "2"],
  "locations": [[0], [0, 1]],
  "U1": [0, 1],
  "U2": [1]
}
```

The four-seed solver outputs an `alpha` certificate with pure customer assignments. The bounded-overlap solver also uses `alpha`, but its assignments may be mixed and its optimality relies on the complete support-interval proof. The shared solver uses `factor` and a separate certificate format; the schemas must not be interchanged. A verifier checks one selected on-path outcome and every actual unilateral deviation, not the universal theorem or optimality of an exact solver.

## Shared-catalog algorithm and certificate

## Exact input contract

Run from the repository root with Python 3 and no third-party packages:

```bash
python3 common_phi_algorithm.py examples/shared/tiny.json --output certificate.json
python3 verify_phi_certificate.py examples/shared/tiny.json certificate.json
```

The JSON input has `weights` and `locations`:

```json
{
  "weights": ["1/3", 2, "0.125"],
  "locations": [[0, 1], [1, 2], [0, 2]]
}
```

- Customer and location IDs start at zero. `locations[j]` lists all customer IDs able to use site `j`. An empty site and an uncovered customer are allowed. `weights` must be positive integers, exact rational strings or decimal strings; the CLI parses JSON decimal literals exactly. Programmatic Python callers should avoid binary floats.
- Both facilities can choose **every** listed site. To restrict both to the identical subset, give equal nonempty arrays `U1` and `U2`. Different subsets violate this algorithm's theorem and are rejected; use `facility_spe/heterogeneous_two.py` for the separate factor-2 model.
- All covered customers must participate. Each customer minimizes expected *realized weight on its chosen facility*; each facility maximizes its expected served weight. Customer randomization is independent. No travel distance, opening cost, capacity constraint, optional service, third facility or site-specific customer cost is included.
- The program writes exact rationals as strings (`"3/7"`, `"2"`). Its reported `factor` is a certificate for that solution, at most `phi`; it is not generally the best factor available in the instance.

The output includes one on-path layout and customer probability vector, one exact customer NE for each **actual** unilateral facility deviation, the menu response cycle and a polynomial default continuation rule. The verifier recomputes loads, each customer's conditional best response and all unilateral payoff inequalities directly from the input and certificate. It imports the same verification function as the constructor, rather than providing an independently implemented checker. A successful check establishes the reported factor for that particular input; independent external proof review of the universal theorem is pending. The free-text default-continuation metadata is not checked; the prescribed default rule is defined in `facility_spe/shared_phi.py` and the proof note: guard-repair the assignment putting all shared customers at facility 1.

## Evidence and operational limits

Run `python3 -m tests.test_shared_phi` for the recorded seeded tests and `python3 -m tests.audits.shared_menu` for the exhaustive small cases. The latter can take longer. The fast program's `O(N^2(n+1)^4)` bound counts rational arithmetic; exact rational operations have polynomially bounded but nonconstant bit cost. The implementation has no published large-instance benchmark or resource cap. Inputs are trusted research inputs rather than adversarial service requests. The integrated paper and menu-completeness proof await independent external review.

Use the exact local/global optimum solver only when needed: `python3 -m facility_spe.exact.mitm examples/shared/tiny.json` is exponential in the number of common customers, but gives an instance-optimal factor; `facility_spe/exact/bounded_overlap.py` is exponential in maximum pair overlap. These are not interchangeable with the fast universal construction.

**Reuse status:** the repository has no chosen public license, stable package API or external proof approval. The exact CLI and verifier are useful for research instances satisfying the contract above; anyone planning to embed the method in a service should independently validate the mathematics, measure memory/time at their input sizes, and arrange an explicit license.

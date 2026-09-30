# Using the shared-catalog research algorithm

## Exact input contract

Run from the repository root with Python 3 and no third-party packages:

```bash
python3 common_phi_algorithm.py astra_ring/example.json --output certificate.json
python3 verify_phi_certificate.py astra_ring/example.json certificate.json
```

The JSON input has `weights` and `locations`:

```json
{
  "weights": ["1/3", 2, "0.125"],
  "locations": [[0, 1], [1, 2], [0, 2]]
}
```

- Customer and location IDs start at zero. `locations[j]` lists all customer IDs able to use site `j`. An empty site and an uncovered customer are allowed. `weights` must be positive integers, exact rational strings or decimal strings; the CLI parses JSON decimal literals exactly. Programmatic Python callers should avoid binary floats.
- Both facilities can choose **every** listed site. To restrict both to the identical subset, give equal nonempty arrays `U1` and `U2`. Different subsets violate this algorithm's theorem and are rejected; use `asym_research/r_menu_solver.py` for the separate factor-2 model.
- All covered customers must participate. Each customer minimizes expected *realized weight on its chosen facility*; each facility maximizes its expected served weight. Customer randomization is independent. No travel distance, opening cost, capacity constraint, optional service, third facility or site-specific customer cost is included.
- The program writes exact rationals as strings (`"3/7"`, `"2"`). Its reported `factor` is a certificate for that solution, at most `phi`; it is not generally the best factor available in the instance.

The output includes one on-path layout and customer probability vector, one exact customer NE for each **actual** unilateral facility deviation, the menu response cycle and a polynomial default continuation rule. The verifier recomputes loads, each customer's conditional best response and all unilateral payoff inequalities directly from the input and certificate. A successful check establishes the reported factor for that particular input, even while the universal theorem undergoes external review. The default rule is defined in `common_phi_algorithm.py` and the proof note: guard-repair the assignment putting all shared customers at facility 1.

## Evidence and operational limits

Run `python3 test_common_phi_algorithm.py` for the recorded seeded tests and `python3 common_phi_counter_audit.py` for the exhaustive small cases. The latter can take longer. The fast program's `O(N^2(n+1)^4)` bound counts rational arithmetic; exact rational operations have polynomially bounded but nonconstant bit cost. The implementation has no published large-instance benchmark or resource cap. Inputs are trusted research inputs rather than adversarial service requests. The integrated paper and menu-completeness proof remain under external review.

Use the exact local/global optimum solver only when needed: `python3 astra_ring/mitm_solver.py astra_ring/example.json` is exponential in the number of common customers, but gives an instance-optimal factor; `asym_research/bounded_overlap.py` is exponential in maximum pair overlap. These are not interchangeable with the fast universal construction.

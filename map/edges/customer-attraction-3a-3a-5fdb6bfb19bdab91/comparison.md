# actual-path node-reply menu/cone: comparison and boundary

## Core result

The assigned object is a finite customer-attraction model with a finite nonempty labelled catalogue and a coverage map. Providers of unit weight move in a fixed order, observe the full ordered history, and split every covered unit customer's value among all providers covering that customer. Empty coverage, duplicate labels with the same coverage, repeated actions, zero customers, and arbitrary off-path weak ties remain in the model. A full pure SPE is quantified over every ordered history and every unilateral deviation, with the continuation recomputed from the supplied strategy after the deviating history.

For a count state `q`, the set-valued reverse recurrence stores all SPE-realizable terminal counts. A deterministic target selector then records a target terminal `j` at every `(q,j)` node and gives a complete history policy DAG. At position `i`, every forced label `b` is completed by the same DAG to its real child terminal `d_b`; deleting the forced current slot gives `h_i(b)=nu(d_b)-e_b` in the `(n-1)`-competitor background domain. The union of these columns is `M`. `M` is a static menu pool, while the unrestricted static value ranges over every `H_(n-1)` background. The separate `path-only` mode restricts supports to labels used on the actual path and is a different domain again.

The fixed-policy cone uses every recorded real IC row `G w >= 0`. Its normalization `c w = 1` is the welfare of the selected actual terminal under the candidate customer masses. Alternating optimization of customer masses and a query distribution is a finite discovery method; it is not a jointly global optimization certificate.

## Exact finite checks

The independent standard-library audit traverses both frozen JSON files and reconstructs all saved count-state DAGs, actual paths, menus, static saddles, and cone rows without importing the original search code, RNG, SciPy/HiGHS, or numerical LP. It checks 21 four-provider records (11 distinct integer inputs) and 8 five-provider cone records (3 distinct integer seeds), hence 14 distinct integer inputs. The four-provider rows check all 56 legal backgrounds and 6 pure queries per record. The five-provider endpoints check all 126 legal backgrounds and 6 pure queries. All 6,950 saved cone rows and 437,850 coefficients agree with independent reconstruction.

The exact finite values are useful as calibration only:

- The four-provider `best` record has `W=215`, `OPT=253`, and `v_M=z_M=215/4`; its strong difference `W-4 z_M` is zero while its weak difference `W-(4-1/2)z_M` is `215/8`. The 20 bank records have positive strong differences, but they are repeated finite inputs (11 distinct seeds), not a universal separation theorem.
- All eight five-provider cone endpoints normalize to one nonzero customer type and satisfy `W=OPT=1`, `v_M=z_M=1/5`, strong difference zero, and weak difference `1/10`. Their 6,950 nonnegative IC rows certify the fixed target DAG for those endpoints, not an all-input or all-SPE statement.
- The original four-provider file remains marked `EXPLORATORY`, and the original five-provider file remains `UNCERTIFIED_NUMERIC`; the exact audit certifies only the frozen bytes and frozen inputs. It does not retroactively certify the original random search history or floating-point optimization status.

## Comparison boundaries recorded in context

The static mixed-security theorem for unrestricted backgrounds has the domain inclusion `M ⊆ H_(n-1)`, so any menu value `z_M` is at least the unrestricted value `v_n`. This is a domain inequality only. It does not turn a menu gap into a failure of the unrestricted aggregate bridge, and it gives no payment of ordered SPE welfare by itself.

The earlier actual-root tail obstruction and the adaptive decorrelation obstruction use a root-only or differently coupled menu. They therefore cannot be identified with this object’s union over all actual positions. Conversely, this object’s finite menu audits cannot repair those obstructions or prove a global bridge. The on-path `menu-cone-best-185` file is explicitly only a first-deviation menu, with a floating-point query and no full-BR claim; it is a scope check, not a theorem or counterexample for this object.

Because this task declares no `read_object_ids`, no cross-object logical edge is emitted here. The self `checks/context` edge records the finite-audit contract and the exact places where a general result is still open. The core coverage therefore remains `isolated-after-review`: the object is mathematically well-identified and its fixed records are audited, but the assigned comparison did not certify a new general SPE, aggregate-security, or six-provider-half implication.

## Open obligations

A future logical edge would need a separately declared endpoint and a complete proof of one of the following: an all-input payment from actual-position menus to ordered welfare, a bridge from the unrestricted static value to the full SPE aggregate, or a complete-SPE counterexample with all historical IC rows. Fixed menu support, fixed cone feasibility, finite exact saddles, and finite weak/strong gaps are insufficient on their own.

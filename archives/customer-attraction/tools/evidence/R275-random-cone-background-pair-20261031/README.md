# R275 random cone and background-pair finite evidence

This directory preserves the three frozen sources claimed by Boss2 and the two import dependencies needed to interpret the random cone script. The random script samples 20 weight vectors for each of `(p,n)=(5,3),(6,4),(7,5)` and solves a finite LP for each selected target. Its JSON is a floating-point finite search record; `slack=0` is a boundary observation, not a negative bridge failure and not a proof of a universal inequality.

`verify_background_pair_circuit.py` is a separate exact `Fraction` regression. Running it with `PYTHONDONTWRITEBYTECODE=1` returns `status=pass` and `exact_finite_algebra_checks=11984`. The script itself states that the four membership cases carry the general identity; the executable check is finite regression support.

The random search depends on `cone_floor_attack.py`, which in turn imports `floor_scan.py`. The source manifest records the three claimed source hashes and dependency hashes. A full random sweep was not silently re-run to completion in this cleanup turn: the replay attempt found the frozen best boundary record and was stopped by the execution wall, so the object records only that partial replay.

# R275 multigadget exact SPE certificates

`multigadget.py` constructs the finite common-theme instance family and calls the preserved `ExactSPESolver`. The two frozen JSON files are complete ordered-history certificates for `m=3` and `m=4`. The replay uses the already preserved exact-spe model/exact/certificate package and verifies every supplied history and deviation.

The certificates are finite pure SPE witnesses. The source does not claim minimum-SPE welfare, arbitrary `m`, a mixed SPE result, or the six-person half target. The source family is therefore retained as a finite construction and a clean benchmark for later comparisons.

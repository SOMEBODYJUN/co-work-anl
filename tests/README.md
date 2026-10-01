# Reproducible checks

From the repository root:

    python3 -m tests.test_shared_phi
    python3 -m tests.test_heterogeneous
    python3 -m tests.test_four_seed
    python3 -m tests.test_lazy_ring

The first three commands check finite exact certificates and independent small support comparisons; they do not establish the manuscript's universal theorems. Audit enumerators are under [audits](audits). Tests print results by default and leave [frozen run records](../evidence/runs/2026-09-30) untouched; where supported, use an explicit --report path to save a new run.

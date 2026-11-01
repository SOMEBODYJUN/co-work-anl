# next-security bridge_attack evidence manifest

This batch preserves the eight raw source payloads under `original/`, one comparison note per source under `comparisons/`, and the attempted cone-search replay under `replay/`. Raw SHA-256 values are recorded in the per-source receipts. The replay exits with status 1 because the exported script imports a missing `search` module; no numerical output is inferred from that failed run.

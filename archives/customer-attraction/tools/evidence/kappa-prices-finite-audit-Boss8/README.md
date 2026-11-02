# KAPPA prices finite audit

The frozen `kappa_prices.py` source was executed with the preserved exact model/certificate dependencies. Its 13 records over nine inputs and 137 Bellman brute-force checks are byte-identical to the existing `kappa_existing_audit.json`; every `bridge_holds` flag is true. The only prices above one are 38/37, 19/18, and three 45/44 entries. This is a finite executable audit of fixed certificates, not a universal sum-kappa budget theorem.

## Reproduction

From this packet run `python3 replay.py`. It reconstructs the original deep source path in a temporary directory, uses the included `runtime/customer_attraction/` and nine `runtime/examples/` inputs, runs the unmodified frozen program, and compares the complete JSON bytes. No ROOT patch is needed in this layout. The earlier runtime manifest describes the historical ROOT-redirected run; the new replay harness is a separate packaging check.

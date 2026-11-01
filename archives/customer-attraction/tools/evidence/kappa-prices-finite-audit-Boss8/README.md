# KAPPA prices finite audit

The frozen `kappa_prices.py` source was executed with the preserved exact model/certificate dependencies. Its 13 records over nine inputs and 137 Bellman brute-force checks are byte-identical to the existing `kappa_existing_audit.json`; every `bridge_holds` flag is true. The only prices above one are 38/37, 19/18, and three 45/44 entries. This is a finite executable audit of fixed certificates, not a universal sum-kappa budget theorem.

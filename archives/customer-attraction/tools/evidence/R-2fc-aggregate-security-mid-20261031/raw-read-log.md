# Raw-read log

All eight bodies were opened at the raw URL rooted at
`https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/68fad804ec5946cb296f77dc5b336308a66abf12/research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/`.
The browser displayed each complete body; no source bytes were edited. `clean show` was separately attempted and its failed fetch logs are retained in `clean-show/`.

| ID | file | bytes | browser read | salient fields |
|---|---|---:|:---:|---|
| `b5868d5b6d047171afcb` | `dr_n5k3.json` | 324 | true | status enlarged/floating/not CAG; `k=3,n=5,trials=500,seed=22103`; objective `0.0`; completed `500` |
| `d4f16fe38986277d7ce7` | `dr_potential_probe.py` | 7799 | true | diagnostic entry; numpy/scipy LP over enlarged DR potentials; explicit not-CAG module docstring |
| `140e0efe501815fbb2df` | `individual_groups_n3k6.json` | 10580 | true | status enlarged/floating/not CAG; `k=6,n=3,trials=1,seed=22112,policy=groups,first=1`; objective `-0.002645502645502644`; root `[0,3,4]`; completed `1` |
| `f6c01a389ec2b00b8bd4` | `individual_plateau_n3k4.json` | 400 | true | `k=4,n=3,trials=200,seed=22111,no_dr=true,policy=plateau,first=1`; objective `0.0`; completed `200` |
| `438b38ee10dea3418acf` | `monotone_n3k3.json` | 349 | true | `k=3,n=3,trials=100,seed=22104,no_dr=true`; objective `0.0`; completed `100` |
| `7f861b14d37a2154f0a7` | `monotone_n4k4.json` | 349 | true | `k=4,n=4,trials=500,seed=22105,no_dr=true`; objective `0.0`; completed `500` |
| `402c8867973f4b6e276e` | `monotone_policy_n3k5.json` | 384 | true | `k=5,n=3,trials=1000,seed=22107,no_dr=true,policy=monotone`; objective `0.0`; completed `1000` |
| `9ae6d4ae302f52483a13` | `monotone_policy_n4k4.json` | 382 | true | `k=4,n=4,trials=100,seed=22106,no_dr=true,policy=monotone`; objective `0.0`; completed `100` |

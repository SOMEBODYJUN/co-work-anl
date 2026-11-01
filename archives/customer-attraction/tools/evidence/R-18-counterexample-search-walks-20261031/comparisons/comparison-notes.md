# R-18 counterexample-search walks 五源比较记录

| ID | 文件 | 大小 / SHA-256 | 核心结果 | 处置 |
|---|---|---:|---|---|
| `daf1b2e40a5c83fa5223` | walk_m5p7_best.json | 331160 B / `f5800bde7c51f12db89d9eefbf1aa3a0981b0acfcc638f18f4701ba4084419e2` | one exact full-history SPE, W=5, OPT=9, ratio=9/5 | retained |
| `fc653491159cabf3efea` | walk_m5p7_run.json | 75008 B / `10bb173705bace712f7519a73d572ddb2b9044f50ab9ac7dea8884c8e73d994f` | 94 cones/184 records, best=9/5 | retained |
| `355f3aec7ec784a91a3f` | walk_m5p8_diverse_best.json | 554167 B / `be2f913701013adf0969f12d57568fefa59e07c117230bccb3c8510ca400b646` | one exact full-history SPE, W=5, OPT=9, ratio=9/5 | retained |
| `63ce3c4c70b86dd06ee2` | walk_m5p8_diverse_run.json | 122391 B / `36f206650932200234971b477ca0d6437dd9b04175b2b6b1b83d5e4862bc673c` | 144 cones/286 records, diverse=true, best=9/5 | retained |
| `057a91b71d694433d041` | symmetric_projection_exact_obstruction.json | 34220 B / `7a0cf0a32c748d7a46d57a326e4b068d9227e1a0fe45a5f3a995e2a4e3054710` | ABC prefix infeasible for desired path; 9 strict deviations | integrated |

## Walk candidates

m5p7 best has 5 topics? It stores 5 players, 7 topics, five customer types; canonical full-history verification is true. Recomputed W=5 and OPT=9, so ratio is 9/5. m5p8 diverse best similarly has 5 players, 8 topics, five customer types and W=5, OPT=9. Both are actual complete-history pure SPE endpoints, but their welfare ratios remain below 2.

The m5p7 run searches 100 steps, records 94 finite cones and 184 portfolios/records; m5p8 diverse run searches 150 steps, records 144 finite cones and 286 records. Float proposal ratios are stored separately from exact endpoints. Neither run proves a universal bound or searches all strategies.

## Prefix obstruction source

The symmetric obstruction JSON repeats the exact ABCD/ABC prefix result: ABCD continuation is SPE feasible with zero margin; at ABC the desired continuation is infeasible, actual payoff minus threshold is `-4262528025340808635153148385102788890849920`, and V/W/X/Y/T1–T5 are profitable under every SPE reply. This is a designated-path obstruction, not a welfare counterexample or global projection impossibility.

## Relation to prior projection sources

The m5p7/m5p8 walks use the same finite strategy-cone approach as the earlier m5p15 projection page but with smaller topic supports and exact endpoint verification. They supply additional ratio=9/5 finite candidates; they do not improve the prior ratio≈1.35035 m5p15 candidate to 2. The symmetric obstruction is the same semantic object as the prior symmetric audit, preserved here as an independent frozen JSON source.

## Boundary

Five sources support finite exact endpoints, finite cone counts, and one designated prefix obstruction. They do not prove `2W<OPT`, Q-CAG-HALF failure, a universal strategy lower bound, or unrelated-machines conclusions.

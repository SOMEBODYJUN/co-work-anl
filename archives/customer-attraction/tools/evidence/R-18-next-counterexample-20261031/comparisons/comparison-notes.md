# R-18 next-counterexample 八源比较

| ID | 文件 | 结果 | 处置 |
|---|---|---|---|
| 67fa853bf5522ded7187 | cycle_family_search.py | Scout cycle search，依赖缺失，未运行 | integrated |
| 463b872cda6adb87e298 | pair_cone_attack.py | pair fixed-cone LP，依赖缺失，未运行 | integrated |
| c61be686e7d352b310ca | pair_cone_best_5_5.json | objective≈1.39e−17，数值零 | retained |
| e9406fb40ba54a4203ec | search_clone_half.py | clone bridge scouting，依赖缺失 | integrated |
| 0457d204de52e18b6741 | search_terminal.py | self-contained reduced replay；无正 violation | integrated |
| a627c2dcdcead4aebd55 | terminal_best_5_5.json | bridge=1, half=1 | retained |
| 2149f3da374911a9e168 | terminal_best_7_5.json | bridge≈0.81399, half≈1.00595 | retained |
| fb8540bc2e41ff59f186 | terminal_clone_equality_audit.json | m=2…10 九条 valid exact regression | retained |

`search_terminal.py` reduced replay m5p5 20 steps best bridge=0.6, half peak≈1.0936；m7p5 10 steps best bridge≈0.58598, half≈1.00674。所有记录均未产生 bridge violation>1 或 half ratio>2。与现有 strategy-cone/clone audits 一致：LP/scout 候选需 exact full-history 验证，有限 regression 不等于一般证明。

# research_6 本轮稳定交接

Q-CAG-HALF-6 **未解决**。本线程所有计算已停止；没有后台进程或待运行轮次。新增 pooled 字典试验未启动。所有浮点目标攻击均未得到严格目标候选；不把有限阴性计为数学结果。

## 建议保留的最小数学清单

1. `potential_menu_joint.md`、`potential_menu_joint.py`、`potential_menu_joint.json`、`audit_potential_menu_joint.py`、`audit_potential_menu_joint.json`：原983行精确辅助停界及独立18主题100947多重集合审计。原点不是SPE。
2. `potential_menu_joint_private.json`、`audit_potential_menu_joint_private.json`：加入逐位置私有谱后990行的更强精确停界，正文在同一md末段。独立审计确认全部18主题极大、全混合势和完整逐位置私有谱通过；倒二对A6/Ri仍有严格盈利。它仍不是目标反例。
3. `private_shared_omission_tradeoff.md`：已有真实私有谱的解析推论。最优主题先扩到不同极大容器，得到 `mW≥(m−1)Dp+OPT_m`；共享遗漏比例α给正文显式比率。六人maximal-private遗漏占比至少4/5足够half。没有混同内部子主题或opt索引d=1，无新一般付款机制。
4. `paired_esm_candidate.md`：成对势排除接口的准确 **OPEN候选**。A/B是原真实前两行动，重复须两份；等价D_i≥D_(i+2)。无证明、无反例、无合法证书行。

## 可接续攻击接口，均无数学状态提升

`large_catalog_target_attack.py`：18主题大目录真实完整策略锥的有限发现器。单count策略及cap8真SPE终局菜单的(state,target) DAG均可完整覆盖全部有序历史；冻结策略后lazy检查所有IC，另可 `--price` 对全部262143个客户兴趣型定价加列。保留三份小运行json以说明已运行范围。结果离二很远；带定价运行只做有限8轮/策略，负reduced-cost仍存在，不能声称全客户锥已优化闭合。浮点NPZ重复快照已删除，可从脚本重建。

复现已完成范围：

```
OPENBLAS_NUM_THREADS=2 python large_catalog_target_attack.py --steps 5
OPENBLAS_NUM_THREADS=2 python large_catalog_target_attack.py --menus 8 --steps 3 --max-cuts 45
OPENBLAS_NUM_THREADS=2 python large_catalog_target_attack.py --menus 8 --price --steps 2 --max-cuts 75
```

最后一条运行期间后补了独立文件命名和已有列reduced-cost符号自检，不改变定价公式；没有为此次微调另开新攻击轮。所有该类输出只是浮点发现，不是精确SPE反例或固定锥的精确上界。

`catalog_completion_probe.py/json`：浮点补目录构造。初次新Z确能压Ri并保全部六位置safe报价，但Z自身成为更强倒二偏离，贪心下一次LP无解；只说明该次贪心完成失败，不说明所有补目录完成不可能。保留完整小JSON以重现这个具体选择；没有完成末两人或全树SPE。

`make_target_attack_seeds.py`、`seed_full18.json`及三份8主题seed、`target_attack_seed_index.json`：已交research_1/4。主题union/omission生成的是新实例，不保旧点IC或比例；其真正BI修复由相应代理报告，不能重复计数。

父方统一checkpoint；本线程不独立push，不声称远端保存状态。

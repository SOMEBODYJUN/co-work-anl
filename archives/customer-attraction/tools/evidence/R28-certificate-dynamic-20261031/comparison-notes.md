# R-28 comparison notes

## Unique content accounted for

- `audit_empty_dilution_rescue.py/json`：指定旧34客户证书的全历史定义级核验、全端点 `X2` 最小值和空稀释三项 `D/H/G`，整合进正文第1节。
- `endpoint_mix_probe.py/json`、`parking_extra_one.py/json`、`utp_attack.py`、`utp_p5m5.json`：有限负诊断和停止理由，整合进第2节并保留为障碍/有限实验。
- `join_conflict_verification.json`、`verify_join_conflict.py`、`markov_terminal_probe.py`、`graph_conflict_probe.py`：精确 join/Markov 丢失历史状态与图冲突 witness，整合进第3节。
- `blind_tail_cycle_audit.py`、`independent_audit/README.md`、`extra_slot_pure_theta_probe.py/json`：七客户盲审、三份预选 theta 证书和无扩样边界，整合进第4–5节。
- `audit_reply_cycles.py`、`reply_cycle_audit.json`：七客户新循环与既有34客户对照，整合进第4节。
- `FAILED_ROUTES.md`、`certificate/README.md`：本批路线边界、旧例来源和停线理由，整合进第1、2、6节；没有重复扫描旧图或摘要。

## Disposition

全部 20 个源都已全文读取并有稳定去向。正文保留 exact finite checks、conditional certificate checks、finite negative experiments、generic representation obstruction 和 dependency gaps 的不同状态；未把任何一项标成一般 half proof 或新的客户吸引反例。旧34客户 cycle/empty results 与已存旧页存在重复，但本批独有的是独立 definition-level audit 和把三类障碍放在同一来源边界下的比较；因此保留原始脚本/JSON 与本页交叉引用。

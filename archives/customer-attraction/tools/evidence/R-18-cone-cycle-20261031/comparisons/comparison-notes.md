# R-18 cone/cycle 五源比较记录

| ID | 文件 | 大小 / SHA-256 | 结果 | 处置 |
|---|---|---:|---|---|
| `08868cd8604deaef5536` | cone_attack.py | 3077 B / `d01883b0d749b19f90e9b8b260c94aac5cb5b5377faaecbb284515e51074af74` | fixed-cone LP scouting，需 exact/integer audit | integrated |
| `b11182f2a1d2dd4b5597` | cone_best_5_5.json | 912 B / `6812b7ee258478ea2c65ab364ec5133fc010de01c21b9625eecebc91c317d391` | objective −0.0625，408 rows | retained |
| `1f622e0805b6cea2e66f` | cone_best_7_5.json | 2938 B / `ffd191cb28397835a744361944b5e5e2a8e6436fea309651277386b00b44ee5e` | objective −0.01886，1706 rows | retained |
| `8abd9e3c265173dfb777` | cone_walk.py | 2784 B / `6f8583af9b9fb1c8d52bcf1e5c624c930e96bf03bb6243faa53448294dab2623` | boundary walk/cycle LP scouting | integrated |
| `60c6ec5af123aa5f5ab3` | cycle_best_5.json | 345 B / `b7a92543f63fba46733028b892448c248b9e0a72054354ba4dfb8b255cbb65e5` | C2 violation ratio=1，half ratio=1 | retained |

## 数学边界

两个 cone objective 都是负值，没有正 gap proposal；cycle JSON 也没有 ratio 超过 1。保存的 seed/LP weights 只是候选分布，尚未经过 integer clone、full-history certificate 或真实 OPT/W 重算。因此这些结果比已验证的 R-18 walk m5p7/m5p8 endpoint 更弱。

`cone_attack.py` 和 `cone_walk.py` 依赖缺失的 `search_terminal.py`/Scout 实现，本轮没有伪造运行；代码读后确认它们把 LP 作为 scouting，正 objective 才进入 exact audit。与已有 strategy-cone、credible walk、projection m5p15 对象一致：有限 cone 结果不等于真实 half 反例。

本批五源不产生 `OPT/W>2`、完整 SPE 反例、一般 cone bound 或 unrelated-machines 结论。

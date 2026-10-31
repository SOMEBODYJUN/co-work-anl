# 全局尾层与首人门槛：五主源证据

实际claim pushed 406e4f57100ac0a6d8fb9733f4781451337e5f9f，Boss4/synced，唯一capture boss4-r3-credible-next5ap-claim.json。五期望ID与实际claim全吻合后逐源clean show取回、全文读/双冻结核SHA。primary-manifest.json共五源47644B；原件保original/的完整相对路径。37.9KB策略文件所有字段及330计数状态条目另以无损紧凑表全读，未以被截断的打印代替尾部阅读。

对应[全局尾层精确资源](../../../state/计算/全局尾层与早期鲁棒行的精确计数审计--计算.md)及[首人探针/游走资源](../../../state/计算/首人弱覆盖门槛的固定策略探针与计数游走--计算.md)。计数状态、完整有序历史和被代表的比较数量严格区分；没有标签合并，没有完整SPE半覆盖反例。

## 三原入口各一次

三原码都没有文件输入或本地helper；terminal只用标准库，两个发现脚本用numpy/scipy。报告原先不置于replay-tree，原码未改。工作区prepare_and_run.py保每入口唯一execution，已有记录拒绝重跑。

| 入口 | 实际新参数/耗时 | 输出 |
|---|---|---|
| audit_global_terminal_layers.py | 原默认两参数(1,6)/(2,9)，1.0616092681884766秒 | exit0，1704B报告全字节同SHA388d77af23c401fc40ec285316a4ff8cc547074ba6d8f9448ded4f2024603c1b |
| first_floor_probe.py | 原默认cross m3/k6，1.1146047115325928秒 | exit0，56次浮点LP，stdout best4.205623901581722；无冻结stdout primary、无完整精确向量 |
| first_floor_walk.py 5 7 | 默认100步/seed143，15.442265272140503秒 | exit0，100次LP调用，t80达到ratio8，37938B新报告全字节同SHAe8ef2e9f90a844b2fe7249886dff78efca84f8830f58048dfe509992b64e237b |

两个发现入口Python3.12.14/numpy2.3.5/scipy1.17.0，三个stderr均空。报告/原stdout/原stderr/execution分别保replay-terminal、replay-probe、replay-walk；replay-tree保完整源相对路径和原创建输出。冻结walk文件没有历史n/迭代，不能由本次默认100步复现回填旧命令。100次调用也不等于100次LP成功，原码未保存全部状态。

## 一次新的固定输入精确认证

audit_frozen_first_floor.py仅读原冻结五人七标签文件，用标准库Fraction实际执行1次（未计时），不导入原发现码或solver/优化器、不做新搜索。frozen-first-floor-exact-audit.json核全部330计数条目、展开2801有序决策历史、19607含自身比较/16806非自身、另2310计数比较，最小差0；462比较多重集确认OPT8。实际path(3,3,3,1,1)、五收益全1、W5，ratio8<9，half差2。

330是acts数组计数状态条目数，非原JSON显示行数，亦非完整有序决策数。七标签保留：0/1/3/4覆盖同一五客户核心，其余2/5/6各一位单独客户；所有规定动作在核心标签，分布3:262、1:63、0:5。精确认证仅针对软件非单射标签扩展中的原七标签策略，没有机械quotient到集合目录并冒称保留所有历史。

## 数学比较与真实范围

comparison-original/保7181B已处置比较稿global_terminal_depth_obstruction.md及双冻结manifest，非primary、非运行输入。该稿是私有E_j族（固定k比率无界、早期鲁棒仅在实际路径）；本原audit是共享E族（固定k比率趋k+2、审所有早期历史鲁棒行）。新正文独立证明共享E全局性质，未把另一族代充代码伴随证明。两者都保缺早期真实IC，非SPE弱化路径不能改叫原half坏例。

当前银行完整反族已经否定一般弱逐人OPT/(2m−1)从m4起的桥；本有限cross和5/7游走通过不是一般证明。逐人覆盖价格B(u_i)≤W是另一个合同，仍需其自身共同付款。五人half已有独立证明，六人仍开放。完整关系、自查、五receipt及下一候选在同名cleanup工作区。串行复制/推送/done由Boss处理，本文未声明新交付已远端发布。

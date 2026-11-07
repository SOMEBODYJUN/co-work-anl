# 0098单位读出十Claim恢复复核

十个成熟Claim的现候选可原样复用；本轮未发现需要改陈述、状态、版本或证据入口的数学问题。当前已有合法任务 `register-lead-unit-readout-supplement-24`，本地任务状态为 claimed、owner 为 Boss4；这里仅给独立数学反馈，不另写正式batch/receipt、不竞争primary。检查时该任务的正式batch和receipt尚未出现在本clone。

复用 schema2 候选：`research/workspaces/p25-register-v2/Boss5/0098-unit-readout-supplement/batch.json`，SHA256 `069fd013fb69bd875342641d521d7d154a84bebb1748115a1b67ae262e9e8d45`。本轮不复制无变化批次。逐对象完整body/evidence引用及本次canonical快照、精确SHA见同目录 `mathematical-review.json`。

当前canonical中十个精确ID均未出现；因此候选沿十个稳定ID/version1，不应因这次复核新建ID、升级版本或另造主身份。候选十材料与Boss4任务十份path/SHA完全相同，当前八个既有共享owner全部保留；所有十材料字节仍匹配baseline。73次body/evidence引用、15个不同正文/数学证据文件的完整SHA及唯一标题均经只读检查，validate_batch通过（10 objects、10 materials、8 reused existing owners）。这项结构检查不代替下列数学判断。

| 对象 | 本次承重核对与结论 |
| --- | --- |
| `UM-UNIT-READOUT-PRUNED-FOREST-IDENTITY-v1` | C∈[1,2)，r=ceil(k(2−C))；mandatory全部变量、无pins。调度递归仅选原已下传r边，完整回填未选轨/分支，保原外unit注入。反向active负载恰2−r/k。 |
| `UM-UNIT-READOUT-HALF-DENSITY-THREE-HALVES-v1` | 全轨全部实际ports逐clause d≤2A；incoming半片先槽、一次共同matching覆盖全部原jobs；非空OPT≥1。split例仅绝对3/2界锐，非通用近似因子下界。 |
| `UM-PRUNED-TREE-LEAF-HITTING-v1` | q=k−r+1；根bad须q个bad children，最小hitting q^h、最大r-free k^h−q^h。双色DP和严格小于dummy条件成立；外资源容量另付。 |
| `UM-UNIT-READOUT-CALIBRATED-SLOT-v1` | 根q是互补selector质量，非根q=t_parent；Σt≥r−1+q等价整数任务数预算L=k−r+1，incoming占首槽；弱Σt≥rq不能代替。强证书仅充分，受限C1必要性另需a d≤A。 |
| `UM-UNIT-READOUT-BOUNDED-DENSITY-SUBTWO-v1` | D≥2、全轨逐clause d≤DA；k≥D自产x0=1/2证书，r/k>1/(4D)；k<D真实容量匹配成功得路径，失败由mandatory必要路径证OPT=2。无给定YES前提。 |
| `UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1` | T∈[1,2)，s=floor(k(T−1))；共同y/t满足Σ(q−t)+≤sq与外容量 iff CONFIG。局部有理分解/阈值网格LP是数学算法；任意lift需取最小正部或裁剪，边际不是joint law。 |
| `UM-UNIT-READOUT-STRICT-UNIT-GAP-v1` | CONFIG1 iff共同整轨LP(L)。多数轨仅对active轨x0=1，未选轨全父置；k1容量流、k≥2界2−floor(k/2)/k≤5/3。给定LP见证舍入与数学LP后端分开，非任意OPT五三近似。 |
| `UM-UNIT-READOUT-CLOSED-TREES-EXACT-CONFIG-v1` | 单变量且每底父k叶共享独有一台unit。实际OPT=2−1/k；s*=min{0≤s<k:(k−s)^h≤2k^(h−1)}。k≥3的s0不可行，满足(k−1)^h条件时Tconf=1+1/k；近单位阈值不等于严格1。 |
| `UM-UNIT-READOUT-FIXED-HEIGHT-APPROX-v1` | 任意密度全部输入，流必须每变量饱和同一b；真实标记叶仅删除后提祖先子树并保共同外注入。b0证OPT2；ceil(b/2)与整数root严格门槛给1+2^(−1/h)。无给定YES前提。 |
| `UM-UNIT-READOUT-SELECTOR-MIXING-v1` | 给同一原P的p份全部jobs真实C≤1见证，指定每sign被某份覆盖，非空N=k^h≥p。d*≤pA只对指定轨；x0=1、另一轨全父置。锐值是指定profile最优，原P全局OPT1；N<p反例保留。 |

必须继续保留的区别：全轨强证书用两个互补根质量；只有strict-unit/mixing的指定active根取incoming=1。fixed-D及fixed-height叶流均不要求给定完整YES；mixing才要求同一P的全部真实YES、指定sign覆盖及非空N≥p。严格CONFIG1的整轨LP与近单位1+1/k阈值不同；局部配置分解只共享同一组边际，不是一个完整整数调度joint law。含pin三个profile是不同P；unit七变量与外端1/4矩阵也不合并。

四源旧综述的“根incoming=1”“fixed-D依赖完整YES”及叶流/mixing挤在同句，已在候选CALIBRATED、BOUNDED-DENSITY、FIXED-HEIGHT的模型、量词与objections内被精确纠正。复核以正式强计数/叶流正文及原数学比较稿的完整证明为准，不把旧压缩句变成新假设，也不改动原成熟材料字节。

0109混页必须保 `needs-decision`。三个unit/leaf owner可接受本页§1–2；§3 Threshold leaf Hall及§4相关partition/共同边际边界，当前Hall主record `UM-THRESHOLD-LEAF-HALL-CONSISTENT-MARGINALS-PATH-PROJECTION-GAP-v1` 仍未引用本页。已读其主record/body，确认模型是指定core/path分区下的共同leaf-edge marginals与条件matching混合，不是所有core状态或完整matching law。应由该主owner/lead定向接证；在真实接受前不能因unit三项闭合而清整页。

本轮连续读完十份成熟正文、共享UM定义、四份原数学比较稿及Hall主正文，并实读候选四份元数据、当前exact-ID/owner/material记录、合法任务definition与validate_batch/compose相关程序。未重读/重跑原审计程序、巨大JSON或历史运行日志；不把过去作者的执行、盲审或finite PASS冒作本轮新验证。用户500K/300K+200K仅是规划值，实际平台余量未知。

交接：Boss4沿合法任务的正式write_paths完成其批次；lead集成时绑定当时最新canonical SHA，保旧0098/0107/0109 DONE资产，不用本十材料局部增量supersede旧完整任务。此目录只含复核与精确接续请求，未做Git、队列、canonical、凭据或超边操作。

# 全局单行基数过滤与紧凑共享逃逸族的独立冻结审查

boss2内部攻击者先从精确候选独立重构健全性、全池支配、整数与匹配机制，再读取冻结正文和实现。以下范围内未发现仍成立的致命异议；内部审查不构成外部同行评审，不以赞同票、置信度或有限计算替代证明。UM-TARGET-v1仍OPEN，全球新颖性与独立论文价值未认证。

## 1. 实际冻结对象

| 文件 | SHA256 | 本次覆盖 |
| --- | --- | --- |
| `research/current/unrelated_machines/row_count_escape_gap.md` | `78b9b5b9ee288a783b07925834ee064e7bbee2737d306bf69771559887a5cc50` | 第1–5节，含每配置延伸、一般gap上界和旧块cut适配 |
| `tests/audits/unrelated_machines/row_count_probe.py` | `9b33496551a3e2e13b7a0ead33be8ec6c9b3cb90f4393dff79aac01196303746` | 输入、零行、容量、增广、权排序、同步删边及独立oracle |
| `tests/audits/unrelated_machines/compact_count_escape.py` | `c26025314f82ff8a7d53dc0e0d953027a81123b2d9a1b94fa4fe10bc9d9f9e69` | 族、配置、全部pair与k=2全部边真实查询 |
| `tests/audits/unrelated_machines/independent_row_count_escape.py` | `f5de5fc882684ea72bd153be98a0ff6335f716ae37c1bad17178b6612c85ed96` | 审查者独立实现，不导入上述主实现 |
| `tests/audits/unrelated_machines/capacity_one_star_pair.py` | `f2a47ff47c9b03e5eaa2f5e747aa97908ebf35f031677251dbf8257cf489732f` | 实际复用的R–R、V–R耦合代码 |
| `research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md` | `be27a3e92dc1da3050cedb911798fb35b78a370afc011fbe5dde519f7cf31837` | 极小星恢复合同、旧紧凑族与GPC₂定义/公式 |
| `research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md` | `962897812a6eb8e3c27962567625120792bea7407bb2c6598c31dbe2c54c4b0c` | 旧条件块切面机制及随B变化的系数 |

没有重做全部经典ST/LST及文献证明。承重内容变化后须重新核对hash和覆盖。

## 2. 安全过滤、精确优化与位复杂度

对象是UM-GLOBAL-ROW-COUNT-FILTER-v1，不是可行性判定或近似算法。当前T调度每行任务数不超过c_i；正行最小值给floor(T/h_i)，截断n安全，零行最小值取n，空行取0。真实T调度强制j→v时，外送Q及B构成容量匹配，撤离权恰为从v卸下的真实处理量。最大撤离权故给真实v负载下界。同步删除和重算行最小值仍保全部T调度，归纳闭合。候选无需大边；零权、T=0、空任务、单可用机器和大分母没有例外漏洞。接受没有一般调度保证。

槽复制后是横截拟阵；覆盖Q以后，可增加的B是收缩拟阵。非增任务权逐次增广精确，BFS更新没有丢失必选任务。不能推广为任意边权贪心。槽数≤mn、边数≤ne，每查询至多n次增广，查询总数≤e(e+1)。h_i来自输入，floor是精确整数除法，有理权和的公分母位长至多输入分母位长总和。循环、存储、见证和输出均有总输入位长多项式界。

固定同一组全行有效H/c时，全局见证限制到任意子池Q_R、B_R后，其匹配仍在R，且子池未匹配可选权不超过全局未匹配权。故全局查询支配所有子池，反向由全局自身是一个子池。每子池可依据不同任务集合重新提高H的规则不在该等价合同内；最终正文已明确此点。

## 3. 紧凑族、k=2及全部候选攻击

UM-COMPACT-COUNT-ESCAPE-GAP-v1只限制指定必要条件的合取，不是计算复杂度困难性或主目标的否定。

整数下界独立重构：B<θ_k<2使每G、R最多接一单位任务，故至少2k个X留中心；每活跃中心至少两Z外送R，挤出至少一Y到z；z负载至少2k/k=2>B。新增逃逸边后重新证明了下界，没有继承旧族结论。上界选2k活跃块，各送一Z到R、全部Y到R、z空，中心最大θ_k。

全部avoid-v证书逐类核对：删V_a，选2k其他活跃块，本块kZ给R、k−1Y给z；删G，取2k+1活跃块；删R_a,ℓ，使a非活跃，其Y占剩k台R；删z用基线。N−1≥2k及N≥2k+1在k=2成立。其他机器仅满足任务数上界，不要求真实负载≤1。任意候选j取回v后，v仅接j，其他计数只减，覆盖所有small和unit边。

任意C∈C_v(1)延伸句也成立：从avoid-v全分配移走C再完整置v，v恰取得C且真实负载≤1，其他计数只减。不是条件LST/条件配置可行性，也没有指数配置检查的多项式声称。

配置的X覆盖1/k+(N−2k)/N=1，Y/Z覆盖与各机归一成立。G–G用N循环；R–R、V–R只用块内k；V–G式(3)末项非负、精确边际、不双选成立。z恒空使新增pair乘积合法。没有把pair证书提升为共同全局分布。

无极小星/旧单双域规则起点：V删最小后θ_k>1，G为N−1>1，R为2k−1>1，z为N−1/k>1；最小域数≥4。m,n是O(k³)，有限边数8k⁴+4k³+2k²，显式矩阵仍多项式；正文未把总编码误称O(k³)。

## 4. 一般gap上界与旧条件块适配

接受合同包含配置可行性，经典投影和槽舍入给≤2T。若先极小星消元，须用旧恢复合同得max(2T,T)=2T，最终正文已明确。安全删边只限制原合法边。结合族T=1接受及OPT→2，正OPT范围该合同上确界gap恰2；不要求接受单调或阈值有多项式oracle。

块cut是旧机制直接适配，不是新Claim。1≤B<θ_k时，r_B≥2；X在V迫至少r_B个Z外送，k+1个R单位槽迫至少r_B−1个Y去z，X不在V时右侧零。取调度混合后仍是有效边际切面。G的单位槽及X总覆盖给中心X边际和≥2k，z分数负载≥2(r_B−1)≥2>B。B=θ_k时r_B=1，整数上界可行。系数须随B改变，不能把低目标的正系数搬到θ_k。本族未绕过旧块机制；一般分离/统一舍入仍缺。

## 5. 实际核验及独立性

实际运行以下命令，stdout写scratch，没有覆盖旧冻结证据：

```sh
python3 tests/audits/unrelated_machines/row_count_probe.py
python3 tests/audits/unrelated_machines/compact_count_escape.py
python3 tests/audits/unrelated_machines/independent_row_count_escape.py
```

主探针实际覆盖7344个合法小矩阵、34344个独立全分配oracle查询、26624个T可行调度保边检查、5个边界和8个非法输入fixture。主族审计k=2,…,5核全部配置及machine pair，k=2实际运行全部168条存活边的优化查询。

独立实现使用Python 3.12.14、Fraction/整数，无随机seed或容忍误差，不导入主实现。

| 范围 | 实际核验 |
| --- | --- |
| k=2,…,5 | 对37、103、217、391台机器逐一构造全部任务avoid分配，逐任务验域和任务数；任务数40、126、288、550 |
| k=2,…,4 | 全机器配置及覆盖；全部666、5253、23436个pair分类，每块共享支持pair公式精确核边际/不双选，复制机器重标号，其余pair乘积 |
| k=2,…,8 | 逐真实Z/Y转移的R占用置换商DP，求活跃/非活跃块最少z任务，再枚举活跃块总数，核全部μ/k≤θ_k网格，仅θ_k可行 |

DP是实际分配的对称商，不是全调度枚举。族中每真实负载为μ/k，结合已构造θ_k上界，对上述有限k精确确认OPT；不替代全k证明。JSON输出实际参数、代码hash和限制；规范冻结结果由主研究者整合到`evidence/runs/unrelated_machines/row_count_escape_audit.json`。

## 6. 未审与未闭合

没有认证一般近似算法、目标搜索oracle、全部条件块识别/分离、条件LST/配置LP、多机同时真实负载耦合、统一epsilon、全球新颖性、外部评审或论文录用。结构登记和主分支整合不替代数学审查；承重hash变化应重新检查。本次范围内无仍成立的致命异议，不表示这些开放义务关闭。


## 同期半单位成果的合并复核

主研究者已实读同行f68299b的§3a双向归约、承诺搜索量词与冻结审查；这排除旧固定δ<1/2的(Aδ)路线，没有反驳本稿的全局计数反例或安全性。合并后joint_matching_completion_and_block_cuts.md的整文件SHA256为`8cf637c20618062a98d4038e7873987acf06bf426a583a6a678d974d7b103ba3`。上表保留实际受审旧版本hash；已逐字比较本稿承重的§4条件块切面，合并前后该节完全相同，故本稿适配及冻结正文hash不变。共享账本/图保留双方不同Claim，生成稿由共同源重建；没有修改同行证明或冻结运行。

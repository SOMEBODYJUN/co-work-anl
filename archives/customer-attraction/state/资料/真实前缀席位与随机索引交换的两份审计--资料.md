---
id: "customer-attraction/true-prefix-seats-and-random-index-audit-contracts"
kind: "resource"
type_tag: "资料"
title: "真实前缀席位与随机索引交换的两份审计"
status: "full-primary-read-with-exact-domain-and-provenance"
summary: "124客户原输入补全31节点SPE及谱比较；五客户13节点随机位置交换反例、正确uniform符号和末回复表。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_prefix_coupled_seats.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/customer_attraction_prefix_coupled_seats.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_random_position_exchange.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/customer_attraction_random_position_exchange.py"
---

# 真实前缀席位与随机索引交换的两份审计

主源311146e332d3bac3e525（prefix_coupled_seats.py，6583B/124行，SHA1bde7f71…）和24f446797606924d0916（random_position_exchange.py，3691B/94行，SHAe4435ad0…）两冻结版本同字节，全部原代码实际读完。[原件/完整来源](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/source-manifest.json)与真实输入、完整新旧报告分开保全。两程序均仅导入标准库Fraction，不导入作者脚本、模型或均衡验证器；有限数据不替代一般席位证明，也不产生六人half反例。

## 124客户原输入没有策略：如何补全而不偷换

prefix默认只读examples/customer_attraction/prefix_coupled_seats_strict.json（源6d08e55bce1a5336932c，1486B，SHA8fa88f66…）。其中只有实例、目标路径和数值声明，没有完整策略。三名单位提供者、五个共同主题标签0–4，十一种客户兴趣和单位重数为

| 兴趣主题 | 重数 | 兴趣主题 | 重数 | 兴趣主题 | 重数 |
| --- | ---: | --- | ---: | --- | ---: |
| {0} | 15 | {1} | 14 | {2} | 14 |
| {0,2} | 11 | {3} | 15 | {0,3} | 14 |
| {2,3} | 3 | {4} | 9 | {0,4} | 5 |
| {1,4} | 13 | {2,4} | 11 | | |

共124名不同单位客户，重数由range展开，不是有权客户或玩家。真实目录客户集由这些单位编号重建。source raw的目标是(0,4,2)，W95、new127/2、old_combined184/3、gap13/6；全部三条claimed rows实际读完。程序不是通用健壮schema验证器：例如负重数range会丢单位，rows比较使用zip且不独立断言任意输入的行数；本次真实合法输入的类型/全部三行另作明确检查。

对每个有序历史h递归保存所有可实现纯SPE终局M(h)。叶为自身；当前收益门槛是max_a min_(z∈M(ha))u_current(z)，保留达到该门槛的全部行动孩子终局。必要性来自每个偏离子树的最低可实现收益；充分性来自彼此不交的有序子树可独立选最低收益续局。因此本有限菜单未把等计数历史强绑同一平局。

先核目标属于根菜单，再递归build：在指定行动保留目标，其他行动孩子按“当前玩家收益、终局字典序”最小者选完整续局。得到根0；第一步0后第二人4，否则第二人0；全部第三人动作表为

| 首/第二行动 | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 4 | 2 | 4 | 4 | 2 |
| 1 | 2 | 0 | 0 | 0 | 0 |
| 2 | 4 | 0 | 0 | 0 | 0 |
| 3 | 4 | 0 | 0 | 4 | 0 |
| 4 | 2 | 0 | 0 | 0 | 0 |

直接沿这同一完整策略重算全部31有序历史/155含自身比较，124非自身偏离，最小slack0，121严格/34平局（其中31自身比较）；不是严格SPE。实际利润(37,30,28)，和为W95；穷举5³终局，OPT100由(0,1,2)达到。

## 新旧席位谱真正比较了什么

五主题覆盖两两不同且均极大。全局私有块大小(15,14,14,15,9)，实际根覆盖C遗漏的私有块D_a大小(0,14,0,15,0)。旧静态席位为|D_a|/s+|S_a−D_a|/m，s=1至m、m3；15个降序值为

62/3，55/3，15，15，15，79/6，13，13，13，38/3，38/3，38/3，34/3，32/3，9。

实际位置i（从1计）、余r=m−i+1、真实过去负载b_x时，程序重算

$$G_{i,a,s}=|D_a|/s+\sum_{x\in S_a\setminus D_a}1/(b_x+r),\quad 1\le s\le r.$$

全部主题和席位联合降序的第r项为λ_i；direct_i=max_a Σ_(x∈S_a)1/(b_x+r)，old_rank是旧谱第r项，old_max=max(old_rank,direct)。实际利润逐位核u_i≥λ_i≥old_max。

| i/r | 实际u | direct | λ | old_rank | old_max |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1/3 | 37 | 15 | 15 | 15 | 15 |
| 2/2 | 30 | 109/6 | 41/2 | 55/3 | 55/3 |
| 3/1 | 28 | 28 | 28 | 62/3 | 28 |

因此Σλ=127/2、Σold_max=184/3、差13/6；全部每主题G数组、排序谱和31动作保完整报告。它是一个真实单位玩家SPE与谱定义的有限比较，不是从三个位置重新证明任意m的席位定理；source scope明确不重新审核arbitrary-m证明。

main可--output，创建父目录后write_text会覆盖该路径，和其他审计的x拒覆盖不同；本批只给新外部路径，未覆盖旧证据。stdout仅摘要，完整报告另存。本批在全输入先读后新增原CLI一次exit0/0.067秒，完整新报告与旧5758B JSON每个字段相同，补上本代码/真实输入SHA绑定；[命令与报告](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/runs/new-run-summary.json)不伪称旧source已带策略。

## 五客户交换反例：全部13动作和六个真实前缀

random审计内嵌三名提供者、互不交主题A={0,1}、B={2,3}、C={4}。根A；首位A/B/C后第二位分别B/A/A，全部末位动作如下：

| 首/第二 | A | B | C |
| --- | --- | --- | --- |
| A | B | B | B |
| B | A | A | A |
| C | B | A | A |

末位是最佳回复，可选已覆盖主题；AB后选B、BA后选A都是并列合法回复，并非“全部选择未覆盖主题”。直接核全部13有序节点39比较，实际ABB，利润(2,1,1)，W4；全部3³终局给OPT3=5，唯一最优支持{A,B,C}。

随机排列这个最优元组的**索引**并强制前两位，在原策略上继续，六结果为

| 强制前缀 | 真终局 | 首位/最新位收益 |
| --- | --- | --- |
| AB | ABB | 2/1 |
| BA | BAA | 2/1 |
| AC | ACB | 2/1 |
| CA | CAB | 1/2 |
| BC | BCA | 2/1 |
| CB | CBA | 1/2 |

所以E最新=4/3，而全部前缀利润恒3，E前缀/2=3/2，差1/6。随机的是比较索引，真实策略仍区分位置和顺序；唯一最优支持/不交主题不产生交换性。

AB与BA的客户负载相同，末回复不同，末位收益都1、终局调和势都5。按位置看前两席在两叶恰同为(2,1)；按主题身份看A/B原持有者份额互换。合法一般结论只是同负载下末位最优值和最终势相同，不把末回复标签识别成同一个动作，更不能由此交换最新位与平均位。

源码还算真实uniform接口目标nOPT−(n−1)W−Σ_(i,j)V_ij=−4。原候选不等式为这个目标≤0，所以本例有正slack4，**不是uniform接口或half反例**。最大主题/安全值、随机前缀交换和全局覆盖是不同命题。

旧616B结果完整保存source_sha256恰等本e443…且没有项目代码依赖，本批准确复用，新增random原CLI0次；不把39比较和六排列重复计成新独立证据。两个现旧页“末位未覆盖主题”和AB/BA前两位置收益的措辞错误仅给[带旧SHA的修正建议](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/suggested-existing-page-corrections.json)，不直接覆盖其所有权或旧source处置。

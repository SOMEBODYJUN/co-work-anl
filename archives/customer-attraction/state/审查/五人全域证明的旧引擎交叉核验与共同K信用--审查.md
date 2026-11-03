---
id: customer-attraction/half5-old-engine-parser-crosscheck-and-common-k-credit
kind: review
type_tag: 审查
title: 五人全域证明的旧引擎交叉核验与共同K信用
status: full-source-and-record-review;historical-exact-crosscheck;no-new-replay
summary: 保留独立K列重构和旧557引擎上的18新行解析器，解释共享重数、同索引交叠、外舍入及6144完整条件；不冒第二份便携主实现。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/half5_import_audit/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/half5_import_audit/REVIEW.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/half5_import_audit/check_metadata.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/half5_import_audit/metadata_and_K_check.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/half5_import_audit/crosscheck_old_engine.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/half5_import_audit/old_engine_crosscheck.json
---

# 五人全域证明的旧引擎交叉核验与共同K信用

## 1. 对象与当前判断

本页处理同一份 `CA-FIVE-HALF-EXACT-v1` 的两类旧复核：标准库元数据/K列重构，以及在既有557行引擎上独立解析18个新投影的全域交叉核验。两者的源码、报告与两份审查全文实读；**本次原程序、全域审计和新数学检查运行均为0**。已充分处置的原成功运行不重复执行。

定理的数学对象仍是[五人半覆盖](../定理/五人半覆盖--定理.md)：有限单位客户、有限非空共同带标签目录、恰五名单位提供者、每份完整有序历史纯SPE、零背景根覆盖。空主题、同覆盖异标签、重复行动、重复比较索引、零客户和任意平局均保留。六人目标及有背景五人利润不由本包推出。旧稿“停止五人研究”的工作安排是原历史，不是本次清洗的停止条件。

证书字节SHA为 `395e056b218d237abe8b85db894f0b1c37d2e14d55c74b1dca723abeceb6a44e`。完整证明和53个整数权已在主定理，局部真实节点详见[独立局部重构](五人局部组件独立重构的真实节点门槛与复现范围--审查.md)。本页补的是这两段具体实现的义务与输入身份，不声称重新发现定理、外审或世界新颖性。

## 2. 共同K列为何是独立承重项

令 \(K\) 为同一目录最大主题大小，各非负必要行写作

\[
S_j=\sum_xa_j(\omega_x)+k_jK\ge0.
\]

证书给53个严格正整数 \(L_j\)，共同分母 \(D=10^{22}\)，目标分子为 \(2D\)。每个客户的完全清分母余项是

\[
R(\omega)=120\left[2D\mathbf1_{\rm covered}-D\mathbf1_{d>0}-\sum_jL_ja_j(\omega)\right].
\]

K没有在每个客户类型中重新挑选。其唯一全局列满足

\[
\sum_jL_jk_j=-2264870,
\]

从而

\[
120D(2W-O)=120\sum_jL_jS_j+\sum_xR(\omega_x)+271784400K\ge0.
\]

这里 \(O\) 是任意五比较主题的并集大小；取最优并集得定理。负的加权K列移到恒等式右侧才成为正信用。不能把每条含K行各自解释为另一份最大主题预算，也不能去掉MAXROOT的负K项。

### 标准库元数据程序的准确合同

`check_metadata.py`共2851B，仅用Path、Fraction、ceil、JSON、hashlib，不导入主核验器、局部核验器或旧引擎。它按原 `MANIFEST.json` 逐成员核大小/SHA，保存结果为21文件；MANIFEST自身不是自己的成员。另核证书字节SHA、53个严格正整数、\(D=10^{22}\) 和目标精确2。

程序从局部有理输入重构K系数：BG先取BG2原索引 `[0,1,3,5,11,12]`，再取BG3前三项；PC先五个PC2再三个PC3；DEEP取各 \(\beta\)；MAXROOT取第一个组件带符号C。缩放 \(s=10^6\)，公式为

| 行族 | 重构 \(k_j\) |
|---|---|
| `MAX` | 1 |
| `DEEP:i` | \(\lceil s\beta_i\rceil\) |
| 固定 `BG:i`、`PC:i` | 相应局部K系数的 \(\lceil s\kappa_i\rceil\) |
| AB/AE/Sbranch索引族的BG/PC | **5倍**对应已向上取整K系数 |
| `MAXROOT-NEW` | \(\lceil sC\rceil=-7412362\) |
| 其余35条活跃行 | 0 |

带索引族先取整再乘5，与先把5吸收到系数再另取整不是同一规定。本次保存的全部18个非零K值为：

| 行名 | K整数系数 |
|---|---:|
| `MAX:fixed:2` | 1 |
| `DEEP:0:5:3` | 2514500 |
| `BG:0:6:7`、`BG:0:7:6` | 各261819 |
| `BG:2:3:4` | 261403 |
| `BG:4:5:3` | 257873 |
| `MAXROOT-NEW` | −7412362 |
| `AE:BG:0:eq:2:1`、`Sbranch:BG:0:eq:2:3` | 各1309095 |
| `PC:0:6:7` | 113336 |
| `PC:2:7:6` | 122302 |
| `PC:3:7:6` | 115272 |
| `AB:PC:5:eq:2:1` | 238100 |
| `AB:PC:6:eq:1:2`、`AB:PC:6:eq:2:1`、`AE:PC:6:eq:2:1` | 各250000 |
| `Sbranch:PC:1:eq:3:2` | 561790 |
| `Sbranch:PC:7:eq:3:2` | 203125 |

报告同时保全部35个零系数的具体行名，不因零而丢掉行身份。程序将整个53键字典与 `active_k_columns.json` 精确比较，再做加权和。它核的是元数据、缩放和这一列，**不核其余客户系数域，也不独立证明每条行的SPE语义**。文件哈希匹配说明所读成员与声明一致，原ZIP来源关系另见导入链审查。

## 3. 旧557引擎上的18新行解析器

7270B `crosscheck_old_engine.py` 不导入新包的 `verify_certificate.py`，但导入旧 `R-c473.../round4_pricing/full_pricing.py` 并继承其 `Universe(overlap=1)`。原程序的这种依赖是明示的；它是独立parser/特征路径，不能叫第二份完全自足便携主实现。

旧引擎承载35条活跃原节点/菜单/PAIR行。`overlap=1` 保留强末两人式的一份比较交叠，与主证明强PAIR相符，不能改用扣两份交叠的普通利润税。新程序从证书行名找出不在旧557名表内的18条行，并独立实现MAX、DEEP、BG、PC与MAXROOT。

### 外舍入与源角色

`tables()` 从原有理组件重建BG9表、PC8表和DEEP3表，逐元素对照原 `row_manifest.json`。左侧收益/K系数ceil、右侧逐会员信用floor，因收益、K及客户数量均非负而只减弱行；负系数同样按这个方向处理。

PC2的 `u_coefs` 仅为附加价格，代码在零起索引1再加 \(10^6\)；PC3的 `u_coefficients` 已含第三位源收益，不再次添加。BG以真正源角色位置1或2取实际份额，PC信用用 `ABCDTQ` 会员序。这里的数组位置不是随意按浮点值排序。

固定客户十位顺序为 `ABCDEUVWXY`。主行客户部分

\[
a_{\rm MAXROOT}=46313177\,u_{1,x}-10^6\mathbf1_{d>0}
\]

另有上一节的 \(-7412362K\) 全局项。DEEP固定行的客户项为

\[
\alpha u_{1,x}+\gamma t-10^6q+(10^6+\zeta)tq,
\]

BG/PC固定行是源价格组合 \(u\) 减 \(\gamma(2t+q)\)。K不在这些客户项中重复出现。

### 同索引信用的四值展开

设一个索引族的四个整数信用值为 \((g_0,g_1,g_2,g_3)\)，五个比较索引上的会员为 \((t_i,q_i)\)。该行客户部分准确是

\[
5u-5g_0-(g_2-g_0)\sum_it_i-(g_1-g_0)\sum_iq_i
-(g_3-g_2-g_1+g_0)\sum_it_iq_i.
\]

代码分别将两个count特征与**同索引交叠**特征乘120送进旧引擎；不能把最后一项换成两个计数之积，也不能让不同族各选不同的最优比较重数。`atom_rows()`另写直接按整直方图求 \(5u-\sum_i\gamma(t_i,q_i)\) 的接口；本报告的 `run()` 实际走完整定价器，并未声称另执行了所有直接接口交叉测试。

## 4. 6144是全部外条件，不是6144个小博弈

外条件是1024个十位会员掩码与共同 \(d=0,\ldots,5\)。固定外条件后，AB/AE各为总数5的八格直方图，完整全集各792个；Sbranch为十六格、全集15504个，均按首坐标计数等于同一d过滤。原策略一定给这些类型中的一个；允许族间更多独立性只扩大核验域。

对旧末菜单，\(0\le h\le d\)、\(0\le\ell-h\le5-d\)，仿射目标的全域最大在

\[
(\ell,h)\in\{(0,0),(d,d),(5-d,0),(5,d)\}
\]

取得。d=0或5时角重复不漏域。给定外条件后，加权行分为固定块、三个各自完整直方图块、三个仿射菜单块，才可分别最大化再加。`query_equal`与offdiag保留原索引相等/不等关系，直方图代表不等于假定匿名策略。

为检查 \(2D\,\mathrm{covered}-D\,\mathrm{opt}-\sum L_ja_j\) 的最小值，必须最大化被减的行和，源实现方向正确。调用为 `price(..., integer='object', objective_scale=D, batch=20)`，主权及乘积使用Python任意精度整数；没有在最后以浮点容差判号。121个缓存context不是客户数、目录大小或全域条件数。

## 5. 两份保存结果及准确执行边界

元数据报告为21成员、53正权、加权K为−2264870、清分母信用271784400。旧引擎报告为6144完整外条件、最小整数余项0、负类型0、121context，原记录26.611693382263184秒。

两报告的 `code_sha256` 分别精确等于本批冻结的2851B和7270B源码字节SHA：`f22983595769c90a17dfd1af956409a086ed31b1befebf3691d4bcda9cd6f3b1`、`63c7c5682994509c1a1dff3adf39246e958fd63693f4a5f1afc99d6660a9472a`。这项当前字节比较不等于重新运行它们。旧引擎报告未保存全部传递依赖的运行SHA、软件版本和完整argv，不补造这种绑定。

两个入口均有main guard；真正运行会覆盖同目录报告。它们仍以旧 `customer_attraction/__init__.py` 为根标记，并读取旧包与旧定价目录，不能在归档证据中盲目原位执行。当前规范证明包、此前已整理的旧557代码/依赖路径及各自SHA见[证据说明](../../tools/evidence/half5-import-audit-and-acceptance-primary/README.md)。本次不重跑21成员审计、53列算术或6144域，不把读取加算新成功事件。

旧6750/7497必要点可以违反新的投影行而仍满足旧系统；它们不是完整SPE反例。源稿提到旧7497点的13条负新行属于另一份具体输入/诊断，本页仅保存其比较关系，没有重授该未在本批主源中的点审计。[最终验收记录](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/aa1882f99bfaf4e97483.md>)继续保存原主程序两次同实现报告、局部36记录与各报告的不同责任。

---
id: unrelated-machines/composition-review-two-actual-witness-presence-gluing-scope
kind: review
type_tag: 审查
title: 两实际见证presence胶合的锐界与后重中端范围
math_scope: ordinary-UM-given-two-actual-schedules-and-two-presence-bits
status: proved-scoped-gluing; later-heavy-medium-separate-identity
summary: 保真实unit匹配分量与virtual原任务恢复、uniform逐k锐界和tiny加权半整化；后heavy-medium带间隔仍可逃逸，不把裸presence升级身份锁或未知见证算法。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/composition_decoder_obstruction_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/composition_decoder_obstruction_review.md
---

# 两实际见证presence胶合的锐界与后重中端范围

## 原审查与三种不同时间合同

composition review全文实读，本页承担UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1及其tiny推广。另全文读当前183行canonical0b9ab7d50bba3b4b7c5825c6208e51d23d20cdb5460d8e7478a6ef866f986e00，工具聚合最初少144 tokens已显式补读1–18行；并全文比较[原证/范围页](单位占位两见证胶合的原证与范围推进--审查.md)。后来heavy-medium §8是比较后续，不倒填旧composition审者已读。

uniform：合法显式P全部有限时间{1,1/k}，二进制k≥2，输入**同一P两份完整实际σ0、σ1**，峰≤T=1+1/k<2。unit-presence U_i指机器是否接一件时间恰1原任务，不指定哪件；允许同job两见证small↔unit切换、任意资格数。不同v,w在σ0均0、σ1均1。可对全部四位向量构造完整原任务σ，

$$C_{max}\le B(k)=1+\lceil(k+2)/2\rceil/k\le3T/2.$$

k2/3的B2，k≥4时≤9/5<2，趋3/2；不宣称所有k绝对次二或一般3/2算法。00/11直接用输入实际见证。

## 真实unit匹配与所有原任务的恢复

每σ的unit job—machine边是一份matching：job一次，T<2使机至多一unit。共同边固定，其余并图为交替路径/偶环：machine–machine路径两端presence相反、至多一0→1测量端；job–job路径两方向各恰一原端点job走已知small；job–machine路径active同时占job端和machine端、inactive使其job走small；内部job始终unit。并图外job两见证均small。

对mixed令v要0、w要1。若v在job–machine路径，从σ1翻此分量inactive，只新增一枚原端点job的small成本1/k，unit内部时间不变；w在另一分量，峰≤1+2/k≤B。否则v在machine–machine分量选0，w另一分量选1/active，其余machine–machine/环任取，所有job–machine分量active。

剩余items为small–small真实jobs及每job–job路径一个virtual选择（两选项是该路径两方向各留下的**不同原端点job**的真实small端）。virtual不是新增执行任务，选它便恢复整条路径全部原jobs。重合机器也合法。

每item两个选择各半，同机合并。令μ_i为该共同半流的small件数，两见证small数s_i^0/s_i^1，则μ_i≤(s_i^0+s_i^1)/2，因全部active只删非负half small。机器容量ceilμ_i的二部整数满流给同时选择，随后解码原路径。11行small≤1、最终峰≤T；00行small≤k+1且不会新增unit、峰≤T；变化行small≤ceil((k+2)/2)、unit≤1，峰≤B。全机而非仅测量端受控。

当前另有独立整数费用流证明：每机unit-cap1、总任务cap按00/11/变化取k+1、2、h+1（h=ceil((k+2)/2)）。两实际见证半混合可行，变化行总数均值≤(k+3)/2。固定σ1在某测量v的unit job留v，半流到全流只加1/2、余量够；另一测量w的unit流仍1/2。余网络仅给w-unit入口费1，整数最小费≤分数费1/2，非负整数迫费0，补回固定job即v1/w0。容量同样给B。这是同合同另一证明，不冒称原virtual证明中已经包含它。

## 四机逐k锐族与真实OPT

P,Q,M,N四机，两unit-only任务x可P/M、y可Q/N；两组各k+2件small-only分别可M/Q、P/N。σ0令xP/yQ，各组在无unit端k+1、有unit端1；σ1令xM/yN反向分配。峰均恰T、测量M/N为00/11。

mixed10强制xM/yQ，第一组两可用机均unit占位，鸽笼迫一机≥ceil((k+2)/2)件small，所以峰≥B；把各组尽量平分达到，mixed01对称。故两个mixed的最优值恰B。总工作量4T、四机给OPT≥T，两strict见证达到；是胶合的锐局部成本，不是一般实例近二gap。族有2k+6真实jobs，按O(k)显式规模收费，不按bit(k)免费输出k件任务。

一般构造只扫输入两份见证、≤2n条unit边及≤n个small/virtual items，流容量截item总数，分母至多2，不按k或其倒数造槽。需要实际见证作为输入，不能用于寻找未知YES、给NO源凭空造strict见证，或保全部job身份/外部位置。

## 不等tiny端的共同加权半整化

tiny身份另给0≤a<1、所有有限时间{1}∪[0,a]，两份峰≤T=1+a。同unit分解仍有效。任意两选择item端成本≤a，可不相等；同机选择较便宜端，不增半均值。其余逐机把incidences按成本降序相邻配对，再与每item的job对组成路径/交替偶环，一次二着色选一色，使每item恰一个原端、每机器配对恰一端。成本q1≥q2≥…的机器相对半均值多至多

$$(q_1-q_2+q_3-q_4+\cdots)/2\le q_1/2\le a/2.$$

奇尾按正项，交错和界由q2≥q3等给出。是同一共同整数选择，不是逐机独立期望。把此用于真实small及job–job virtual items，恢复全部原任务：11行总负载≤1+3a/2，变化行≤1+(1/2+a)+a/2=3T/2，00行≤1+3a/2；单分量翻转时≤1+2a≤3T/2。a0无需除法；任意不同tiny也统一3/2T。

奇k的uniform锐族满足B=3T/2，k→∞同时a→0，所以统一系数不可降低；不称每固定a都锐。a<1/3给绝对峰<2，a1/3的k3例mixed2，端点不能偷加。

## 后续有间隔heavy/medium：引入medium本身不充分

当前§8另立UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1。两strict见证峰≤T>0，仅其实际所用端在medium[0,aT]或heavy[(1−ε)T,T]，0≤ε<1/2、a<1−ε；未用端任意。给同样两测量heavy-presence00/11，可仅用每job两见证端胶合到

$$[3/2+(\varepsilon+a)/2]T=[2-((1-\varepsilon)-a)/2]T<2T.$$

匹配仍由2(1−ε)>1成立；内部翻分量heavy成本可增εT，不能沿unit“内部不变”旧句。否则用同加权配对，11/变化/00三类完整负载分别≤(1+ε+a/2)T、上式、(1+a/2)T。固定端点gap≥κ给2−κ/2保证。无新软件/有限实验。

这正限定旧composition的“需medium/身份/共享锁”等下一义务：medium若仍留上述间隔和裸presence，两actual见证依旧可逃逸；不能把建议当充分hardness构造，也不把后续证明追记为旧审者已盲审。无跨模块锁/任务身份固定的裸读出被此类胶合阻断，不排其它源相关decoder或一般算法。标准matching/flow工具不认证新颖性，旧历史scratch枚举非本批新run。[原件/实际范围](../../../../tools/evidence/um-foundation-composition-configuration-reviews/README.md)。

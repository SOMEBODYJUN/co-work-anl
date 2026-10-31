---
id: "customer-attraction/optimal-union-incidence-lp-actual-prefix-envelope"
kind: "lemma"
type_tag: "引理"
title: "最优目标并集关联LP的真实前缀包络"
status: "complete"
review_level: "full-source-read-and-self-contained-mathematical-reconstruction"
summary: "将incidence预算限制在固定最优并集，显式证明LP客户支付与真实同路由后继支配的后缀归纳，不免费得到一般half。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/shared_omission/target_union_incidence_budget.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/shared_omission/target_union_incidence_budget.md"
---

# 最优目标并集关联LP的真实前缀包络

## 目标、极大主题和LP

采用共同目录单位客户、单位提供者、全部有序历史纯SPE，根人数m≥1。固定一个最优m主题组合的并集O，记o=|O|。o=0时W≥0直接成立，以下o>0。将不同覆盖集合取包含极大者B_1,…,B_s（只用于路由/预算，不删除原动作或合并策略历史）。给每个原主题固定一个包含它的B_j作为路由。

每个x∈O的极大归属I_x={j:x∈B_j}非空，w_I=|{x∈O:I_x=I}|。前缀长t时，p_j为过去动作路由到j的次数，Σp=t，剩r=m−t≥1，p_I=Σ_{j∈I}p_j。定义
\[
 f_j^O(p,r)={w_{\{j\}}\over p_j+1}
 +\sum_{I\ni j,\ |I|\ge2}{w_I\over p_I+r}.
\]
只有目标客户被计入，实际偏离选择的仍是**整个合法主题**B_j，不能删掉O外客户或限制博弈动作。

有限关联LP
\[
 B_O(r)=\min\sum_j\beta_j,\quad\beta_j\ge0,\quad
 \beta_j\ge1\ (w_{\{j\}}>0),\quad
 \sum_{j\in I}\beta_j\ge r\ (w_I>0,|I|\ge2).
\]
无该类型就不虚加约束。β全取r可行；将任何坐标截到r仍可行，因此最小值在紧集[0,r]^s取得。o>0保证B_O(r)>0。LP是证明的实权，不改变单位客户模型。

## 客户级预算：任意路由前缀都有效

取最优β，y_j=p_j+β_j。对单例归属，目标客户在Σ_jy_j f_j中贡献(p_j+β_j)/(p_j+1)≥1；对共享I贡献(p_I+Σ_Iβ)/(p_I+r)≥1。因此
\[
 \boxed{o\le\sum_jy_jf_j^O(p,r)
 \le[t+B_O(r)]\max_j f_j^O(p,r).}\tag{A}
\]
原稿把整个二段链写为“对任意可行β”；第二段作为这个全称断言不成立。例：两个不交单客户极大主题、m=r=2、p=0，B_O(2)=2，f=(1,1)；可行β=(2,2)给Σyf=4>2=(t+B_O)maxf。对任意可行β只能写t+Σβ；本页明确先取最优β，才有所示(A)。这修复中间量词，不改最终包络结论。

## 必须补上的真实后继论证

定义正分母D_t=t+B_O(m−t)，后缀包络E_t=max_{q=t,…,m−1}D_q。对所有有序历史由剩余人数归纳证明当前最终收益≥o/E_t。

在该节点强制选最大f_j的B_j，沿同一σ看真实后继：若没有后继路由j，则目标单例归属客户后来没人能覆盖，分母≤p_j+1；共享客户旧负载≤p_I、全部当前和未来贡献≤r，分母≤p_I+r。故强制者真实收益≥f_j≥o/D_t。

若有后继路由j，取其中一个真实未来行动F⊆B_j。二者在**同一完成叶**中，对F每个客户获得相同份额，B_j还可能有额外客户，所以强制者总收益≥这个后继玩家的完整收益。归纳对该未来真历史给≥o/E_{t'}，t'>t；因E_t≥E_{t'}，至少o/E_t。o/D_t也至少o/E_t。两情形都给强制偏离值≥o/E_t，当前SPE最优性完成归纳；末位没有后继，用第一情形。 原稿第39行把“偏离B_j直接得到至少f_j”写成无条件句也过强：两人、A含2客户、B含1客户且不交，完整策略所有人均选A；此时O=3、根r=2有f_A=2，真实选A后只有收益1。发生同路由后继时应使用上面的收益支配与归纳，而不是声称直接达到f_j。最终o/E_t界仍正确。没有把“强制B_j最优”作假设、没有冻结后继或将同计数历史合并。

沿实际路径求和
\[
 \boxed{u_{current}\ge{o\over E_t},\qquad
 W\ge o\sum_{t=0}^{m-1}{1\over E_t}.}\tag{B}
\]
这是把既有全极大并集的incidence路由法限制在一个固定最优并集的正确接口；即使全目录并集更大也不把OPT换成全并集。

## 精确LP也不保证一般half

若目标有全部两两归属、无目标私有类型，s≥2时β_j=r/2达到所有对约束，总重sr/2。对全部对约束求和，(s−1)Σβ≥binom(s,2)r，给匹配下界B_O(r)=sr/2。s≥2时D_t=t+s(m−t)/2随t不增，E_t=D_t。

为让该示弱例与“目标是最优m主题并集”兼容，可取s=m+1≥3、每对极大主题有一客户、只含这s个主题：任取s−1=m个主题已覆盖全部对客户，各极大覆盖不同且互不包含，因此O确为全客户最优并集。此时
\[
 \sum_t1/E_t\le {2H_m\over s}={2H_m\over m+1}\to0.

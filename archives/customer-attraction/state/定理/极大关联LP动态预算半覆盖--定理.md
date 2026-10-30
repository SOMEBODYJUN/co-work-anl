# 极大覆盖关联 LP 的动态预算界

## 定义

取共同有限目录的不同包含极大覆盖集 (B_1,\dots,B_s)，令
(C=\cap_jB_j)、(c=|C|)、(U=|\cup_jB_j|)。按每个客户属于哪些极大集划分
(X_I) 和 (w_I=|X_I|)。在长度 (t) 的合法前缀中，将每个已选标签路由到一个包含它的极大集；记该集已有路由数为 (p_j)，(r=n-t)，(p_I=\sum_{j\in I}p_j)。定义

\[
f_j(p,r)=\frac{w_{\{j\}}}{p_j+1}+
\sum_{\substack{I\ni j\\|I|\ge2}}\frac{w_I}{p_I+r}.
\]

对每个 (r\ge1)，定义有限覆盖 LP

\[
B(r)=\min\left\{\sum_j\beta_j:
\beta_j\ge1\ (w_{\{j\}}>0),\quad
\sum_{j\in I}\beta_j\ge r\ (w_I>0,|I|\ge2),\quad \beta_j\ge0\right\}.
\]

令 (D_t=t+B(n-t))，再令 (E_t=\max_{q\ge t}D_q)。

## 条件定理

对任意完整历史依赖纯 SPE，当前前缀存在一个合法极大集偏离，其收益至少

\[
\ell_t=\frac cn+\frac{U-c}{E_t}. \tag{1}
\]

证明是对剩余人数的反向归纳。取 LP 最优（或任一可行）(eta)，置 (y_j=p_j+\beta_j)。私有块满足 (y_j/(p_j+1)\ge1)，非私有关联块满足
\(\sum_{j\in I}y_j/(p_I+r)\ge1)，故

\[
U-c\le\sum_jy_jf_j(p,r)
\le (t+B(r))\max_j f_j(p,r)
\le D_t\max_jf_j(p,r).
\]

若偏离后某个后继被路由到同一 (j)，取第一个这样的后继并应用归纳假设；偏离者选择整个 (B_j)，包含该后继主题，于是逐客户收益支配其末局收益。若没有这样的后继，分母界直接给出 (1)。SPE 最优性把偏离下界转回实际行动。这个论证保留完整原续局、全部有序历史和任意平局。

根部求和得到

\[
\boxed{W\ge c+(U-c)\sum_{t=0}^{n-1}\frac1{E_t}.} \tag{2}
\]

由于 (OPT_n\le U)，若右侧系数至少 (1/2)，则该关联类满足 half 覆盖。此定理是结构条件结果，不是无界关联下的全局 Q-CAG-HALF。

## 可检验充分条件

令极大关联超图的分数覆盖数

\[
\tau_{inc}=\min\left\{\sum_j\alpha_j:
\alpha_j\ge1\ (w_{\{j\}}>0),
\sum_{j\in I}\alpha_j\ge1\ (w_I>0,|I|\ge2),
\alpha_j\ge0\right\}.
\]

取 (eta_j=r\alpha_j) 得 (B(r)\le r\tau_{inc})，进而

\[
W\ge c+(U-c)\sum_{r=1}^n\frac1{n+(\tau_{inc}-1)r}. \tag{3}
\]

所以 (	au_{inc}\le2) 时由 \(\sum_{r=1}^n1/(n+r)\ge1/2\) 得 half。若 (	au_{inc}\le3) 且 (n\ge7)，则
\(\sum_{r=1}^n1/(n+2r)>1/2)，也得 half。该条件是极大关联的覆盖数，不是原主题目录的普通分数覆盖数。

例如五个极大集的正关联只出现在
({1,2\},{1,3\},{1,4\},{1,5\},{2,3,4,5\}) 时，
(alpha_1=1,alpha_{2..5}=1/4) 给 (	au_{inc}=2)，但这只对该关联模式及其无其他正块的实例成立。

## 边界

全对关联、无私有块时 (B(r)=sr/2)，LP 系数随极大集数线性恶化；LP 本身无法覆盖稠密高关联的一般情形。系数小于 (1/2) 只是证书模板边界，不是 Q-CAG-HALF 反例。来源 `25f342f9981ec398c1ea` 没有使用有限计算，外部审查与新颖性未认证。

# iid 支持查询平均低于 extra-slot 值的合法两人族

状态：2026-10-23。本文否定一种证明路线，不否定 extra-slot 首位候选或 half。
背景为空；完整两人纯 SPE 及所有末位历史明确保留，任意平局不受限。

## 1. 一般子集设计与精确区间

取 m>=2 个 peripheral 主题 P1,...,Pm 和 hub H。固定 1<=s<m，核心客户对应所有
s 元 peripheral 标签子集，每个子集可复制 a>=1 次；这些客户喜欢 H 和该子集。
每个 Pi 另有 P>=0 名私有客户。均为不同单位客户。记

\[
 M=a\binom ms,\quad d=a\binom{m-1}{s-1}=Mt,\quad
 e=a\binom{m-2}{s-2},\quad t=s/m,
 \quad G=g_3(1/m),\quad g_3(z)=1-z+z^2/3.
\]

s=1 时 e=0。对 q_H=0、q_Pi=1/m，三人静态 iid 查询收益为

\[
 \alpha_H=M g_3(t),\qquad
 \alpha_{P_i}=d g_3(t)+PG=\lambda.
\]

故 q 是静态对称混合 Nash 当且仅当

\[
 P\ge L_N:=\frac{(M-d)g_3(t)}G. \tag{N}
\]

两人顺序策略定义于全部历史：首位 H；首位 H 后末位 P1；首位任意 Pi 后末位 H。
H 后末位各查询收益是 H:M/2，Pi:P+d/2；Pi 后末位各查询收益是

\[
 H:M-d/2,\quad P_i:(d+P)/2,\quad P_j:P+d-e/2\quad(j\ne i).
\]

因此该完整策略为 SPE 的充分且在指定回复下必要区间为

\[
 \frac{M-d}2\le P\le U_B:=M-\frac{3d}2+\frac e2. \tag{S}
\]

上界保证 H 在 Pi 后优于其他 Pj；它也自动保证优于重复 Pi，
因为 U_B<=2(M-d)。同一上界 U_B<=M-d 保证首位 H 的真实收益
L_H=M-d/2 至少为每个 Pi 的真实偏离收益 D=P+d/2。因此根也最优。
等号时仍允许选择上述真实平局回复，不改动完整 SPE 定义。

所有 q 支持中的真实首位偏离收益均 D。它们的平均低于静态 iid Nash 共同收益
当且仅当

\[
 P<U_D:=\frac{d\,[g_3(t)-1/2]}{1-G}. \tag{D}
\]

右端为正要求 g_3(t)>1/2。故可判别的联合参数区间为
max((M-d)/2,L_N)<=P<=U_B 且 P<U_D；所有重数必须为整数。

## 2. 一键整数无限族

令 m>=8 为偶数、s=m/2，每个核心子集复制三次，

\[
 C=\binom m{m/2},\quad M=3C,\quad P=C=M/3,
 \quad d=M/2,\quad e=\frac{M(m-2)}{4(m-1)}.
\]

总单位客户数为 (m+3)C。由于 g_3(1/2)=7/12，

\[
 \alpha_H=D=\frac{7M}{12},\qquad
 \lambda=\frac{7M}{24}+\frac M3G,
\]

\[
 \boxed{\lambda-D=\frac{M(3m^2-24m+8)}{72m^2}>0.} \tag{1}
\]

m>=8 时分子为3m(m-8)+8>0，所以 q 是 Nash 且 hub 为严格支持外劣回应。
H 后任意 Pi 的末位收益 D=7M/12>M/2，故真实回复 P1 是最佳回应。
Pi 后 hub 的收益为3M/4，而任意其他 Pj 的收益为
5M/6-e/2；两者之差为

\[
 \frac{M(m-4)}{24(m-1)}>0.
\]

hub 也严格优于重复 Pi（后者收益5M/12）。因此 Pi 后末位唯一回复 H。
根选 H 获3M/4，每个 Pi 的真实偏离仅获7M/12，根严格最优。
这穷尽1+(m+1)个决策历史，给出完整纯 SPE。

故 q 平均真实首位偏离收益严格小于 lambda_3，
但真正根收益3M/4仍严格大于 lambda_3，因为G<=1使lambda<=5M/8<3M/4。
这个族否定“将静态 Nash 查询 q 直接平均真实偏离就能支付 lambda”的桥。

## 3. 更小的单个整数实例

m=8、s=4、a=1、P=24 给 M=70、d=35、e=15，总客户262。
完整策略同上；q 为均匀八 peripheral 的静态三人 Nash。

\[
 \alpha_H=245/6,\quad \lambda_3=997/24,
 \quad D=\theta_2=83/2,\quad \lambda_3-D=1/24,
 \quad u_1=105/2.
\]

Pi 后 H 的末位收益105/2，其他 Pj 的末位收益103/2，故 H 唯一最佳回应。
H 后任意 peripheral 是最佳回应，根 H 收益105/2>83/2。
`check_hub.py` 独立从262名单位客户枚举每个比较，包括全部双竞争主题。
`check_family.py` 用 Fraction 对区间、公式、全部两人历史和代表参数做独立精确核验。
后者是实现回归；一般族的依据是上文解析推导。

## 4. 剩余义务

对一般 r=2 的 arbitrary background 和 arbitrary common catalog，extra-slot 仍需证明
首位可选某个行动的真实回复收益至少 lambda_3(b)。本族中支持外高单独收益主题 H
支付这一缺口；其静态 iid 查询收益alpha_H却低于lambda，说明“静态未用主题可忽略”
与“真实分支未用主题无助”不可混同。能否普遍用支持外回应的闭包或势上升支付，仍开放。

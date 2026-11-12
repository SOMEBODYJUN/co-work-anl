# λ 段的完整几何：11面与23顶点

本页对应 [proof.md](proof.md) 第4–6节。两种 $q_0=1/6,1/5$ 都使用四变量顺序 $(\tau_3,\tau_4,\tau_5,\lambda)$，不存在优化器计算。

## 完整半空间

\[
\tau_3,\tau_4,\tau_5\ge0,\qquad9\le\lambda\le16,
\]

\[
\frac34\tau_3+\frac{q_0}{12}\tau_4+\frac{q_0}{6}\tau_5
\le\frac\lambda{20}-\frac{q_0}{2},
\quad
\frac34\tau_3+\frac{q_0}{12}\tau_4+\frac{q_0}{6}\tau_5
\le\frac34-\frac{q_0}{2},
\]

\[
\frac34\tau_4+\frac{q_0}{6}\tau_5
\le\frac\lambda{20}-\frac{q_0}{2},
\quad
\frac34\tau_4+\frac{q_0}{6}\tau_5
\le\frac34-\frac{q_0}{2},
\]

\[
\frac34\tau_5\le\frac\lambda{20}-\frac{q_0}{2},
\qquad \frac34\tau_5\le\frac34-\frac{q_0}{2}.
\]

下界 $\lambda\ge9$ 是本段研究窗口。其他帽面来自单缺真实状态，$\lambda\le16$ 来自全中间会员且末位1的真实状态。

## 三种完整而独立的构造

1. 生成器枚举每域全部 $\binom{11}{4}=330$ 组四面交点，用 Fraction 高斯消元并检验全部半空间。
2. 字面检查器从 $[0,1]^3\times[9,16]$ 的16顶点开始，按六帽面依次裁切。只在两个顶点共享的活跃法向秩为3时判为真边，并在该边上求交。
3. 字面检查器另外直接构造固定 $\lambda=9,15,16$ 的三角递推角。三个方法所得顶点集合逐坐标准确相同。

## 角的统一公式

令 $\alpha=\min(\lambda/20,3/4)-q_0/2$。对 $\varepsilon_3,\varepsilon_4,\varepsilon_5\in\{0,1\}$，依次计算

\[
\tau_5=\varepsilon_5\frac{4\alpha}{3},\quad
\tau_4=\varepsilon_4\frac43(\alpha-q_0\tau_5/6),\quad
\tau_3=\varepsilon_3\frac43(\alpha-q_0\tau_4/12-q_0\tau_5/6).
\]

| $q_0$ | $\alpha(9)$ | $\alpha(15)=\alpha(16)$ | 最大单坐标上界 |
|---|---|---|---|
| (1/6) | (11/30) | (2/3) | (8/9) |
| (1/5) | (7/20) | (13/20) | (13/15) |

上下界不能在同一坐标同时激活，因为所有上界都严格正。因此固定截面恰有8角。两端截面的16角全部是四维顶点；$\lambda=15$ 的每个非零角至少激活一对斜率不同的 A/B 面，多出一条独立法向，产生7个顶点。零角只激活三条 $\tau=0$ 面，仍处在一条直边内部。

## 所有面均不可约

| 面类型 | 每域的面数 | 每面顶点数 | 每面仿射秩 |
|---|---:|---:|---:|
| $\tau_j=0$ | 3 | 11 | 3 |
| $\lambda=9$ 或16 | 2 | 8 | 3 |
| A 帽面 | 3 | 8 | 3 |
| B 帽面 | 3 | 8 | 3 |

严格内点 ((1/100,1/100,1/100,10)) 证明域为4维。各面的秩3证明它们全是真正 facet；没有冗余面。

[necessary_facet_witnesses.json](necessary_facet_witnesses.json) 给出全部22个面的具体有理必要性见证：取该面的全部顶点平均作为相对内点，再沿该面的外法向走一个准确有理小步，保证只违反这一面。真实状态面还保存负的对应成本余项。权非负面和窗口下界分别按其真实含义标注，不误称为隐藏状态必要性。

完整端点、活跃面、独立活跃基见 [parameter_domains.json](parameter_domains.json) 和 [endpoint_table.md](endpoint_table.md)。独立真边裁切每阶段和全部面秩见 [literal_geometry_checks.json](literal_geometry_checks.json)。

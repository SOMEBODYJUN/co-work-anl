# RA12 终审原件先读

复核人 `/root/ra12_visual`，gpt-6.2-sol / max。冻结快照 `f733447a84a1c488a3814b28d1c180ffabb8fd72dbd531426b8e5c16b7465148`。

原始 PDF SHA-256 为 `832de7c38426479bae23211cf7474ea637963941d73ccc3cb5ce7d35be6f9065`。在本轮打开冻结正文前，已逐一重新打开 7 张 400 dpi 整页与 42 张重叠分区，共 49 个原图，逐区记录所见。我此前参加本篇初读、恢复及第二遍复核，本轮顺序为先原图再冻结正文。

第七页整页与六区 PNG 的 RGB 通道极值均为 (255, 255)，从原 PDF 第七页直接再栅格化的每个采样亦为 255。

## p0001

`image:p0001` · `pages/p0001.png`。标题 Littlewood 3 定律，下列近似、连续及收敛三句。有限测度例后接 f:X→Y 的开覆盖拼接，继而局部有限闭覆盖和可测函数近似旁记；没有独立页码或边缘另一证明。

- `image:p0001-r1c1` · `regions/p0001-r1c1.png`。自 Littlewood 标题到三条手写口号及 Ex 的 E∈M、m(E)<+∞，三条均居左。
- `image:p0001-r1c2` · `regions/p0001-r1c2.png`。第一条只重露‘区间’末端，下面横接例题 ε>0、存在有限列开区间和 s.t.；其余空白。
- `image:p0001-r2c1` · `regions/p0001-r2c1.png`。接例题条件、对称差 Δ 后有限并，再至 Lemma 设 f:X→Y 与限制 fα，公式左端上标只见短划邻开括弧。
- `image:p0001-r2c2` · `regions/p0001-r2c2.png`。由例题开区间列转 Lemma 的 X 由各 X_i 开覆盖，右部 f:X→Y 连续及 (限制)^{-1} 清楚。
- `image:p0001-r3c1` · `regions/p0001-r3c1.png`。从‘注意到’、限制连续、各 Xα 属于 τ_X，到闭覆盖条件与末行，函数后两字首字见走之底，要求可数个覆盖。
- `image:p0001-r3c2` · `regions/p0001-r3c2.png`。相对开 C∩Xα 接‘X 中开集’和收尾笔划，后为‘但改成局部有限闭覆盖’及 U 只与有限个 Xα 相交，底部收于‘覆盖’。

## p0002

`image:p0002` · `pages/p0002.png`。Lusin 命题在上，紧接要求闭集构造的句子。以下由简单函数、内正规性和有限并转一般可测函数；本页底只写简单函数序列的逐点逼近，下一页展开。

- `image:p0002-r1c1` · `regions/p0002-r1c1.png`。标题 Lusin 至 E 上 a.e. 有限和误差 m(E\Fδ)<δ，再见‘并给出闭集构造 Fδ 的表达式’。
- `image:p0002-r1c2` · `regions/p0002-r1c2.png`。余下的可测、∀δ>0、Fδ 与 E 之间带‘闭’的记号，f|Fδ∈C(Fδ)，左缘重露‘式’末字。
- `image:p0002-r2c1` · `regions/p0002-r2c1.png`。构造要求重现，P.f.(1) 接 f∈S(E)、代表式 f 后的上下两小点、内正规性、闭集 F_{i,δ} 和下方并号开端。
- `image:p0002-r2c2` · `regions/p0002-r2c2.png`。式字末、存在有限 E_i 及 E=并；手写并后记号像 χ_i，下一行和后面均用集合 E_i，末为 m(E_i\F_{i,δ})<δ/ℓ。
- `image:p0002-r3c1` · `regions/p0002-r3c1.png`。Fδ 定义为有限并，测度误差等式半行，继而 (2) f∈M(E) 及 {φ_k}⊂S(E)。
- `image:p0002-r3c2` · `regions/p0002-r3c2.png`。横接误差并与求和等式并收 <δ，右下为 lim φ_k(x)=f(x), ∀x∈E；外边无他字。

## p0003

`image:p0003` · `pages/p0003.png`。承接一般 Lusin，闭集交、误差行、一致收敛提示；中部写有界化 g 和两条反式；下部以‘或用’开启 Egorov 替代论证并留空一笔至次页。

- `image:p0003-r1c1` · `regions/p0003-r1c1.png`。‘由(1)’接 ∀δ 和 ∀k∈N*、闭包含左边 Fδ，后 φ_k∈C(F_k)，Fδ 为交，误差等式和连续性行首。
- `image:p0003-r1c2` · `regions/p0003-r1c2.png`。首个 δ/2 的 k 位抬高，下一求和的 k 靠基线，后见在交集上连续及‘下证一致收敛’。
- `image:p0003-r2c1` · `regions/p0003-r2c1.png`。从 φ_k 连续过渡至 Egorov 的有限测度条件，f 非有限处的零测量提示，g 的分母 1+|f|，下式 1−g 后面没有绝对值。
- `image:p0003-r2c2` · `regions/p0003-r2c2.png`。连续与一致收敛的句尾、非有限点测度 =0、模长反式 |f|=|g|/(1−|g|) 的右部，右边空白。
- `image:p0003-r3c1` · `regions/p0003-r3c1.png`。‘或用 [Egorov 音写] 定理’、m(E)<+∞、∃φ_k→f，至 ∀δ>0 存在闭 Fδ⊂E 的末行起笔。
- `image:p0003-r3c2` · `regions/p0003-r3c2.png`。只接最末行 m(E\Fδ) 与右侧短横，未见 <δ 或统一收敛在本页被补写。

## p0004

`image:p0004` · `pages/p0004.png`。页首 Egorov 的 Gδ 及 E\Gδ 上一致收敛，闭 Hδ 内逼近、帽 Fδ 和两项误差，下面另起 m(E)=∞ 的环带局部有限拼接。个别留白与严格不等号仍是原笔记草式。

- `image:p0004-r1c1` · `regions/p0004-r1c1.png`。首个‘用’形引 Egorov，其后 Gδ⊂E（对照下一行仍为坏集标签），m(E\Gδ) 留横，φ_k 在 E\Gδ 上一致 f，下一行为考虑的交集。
- `image:p0004-r1c2` · `regions/p0004-r1c2.png`。接上一句的 f，‘由可测的内正规性’填至行末，m((E\Gδ)\Hδ)< 后拖长横而未填写右端。
- `image:p0004-r2c1` · `regions/p0004-r2c1.png`。Hδ 闭包含、F 帽为交、‘要证’的补集并式、原严格小于及 E\Hδ 拆分的左段。
- `image:p0004-r2c2` · `regions/p0004-r2c2.png`。只拼接 Hδ 误差的空格与三行右边括号，末尾右项明确为 Gδ\Hδ。
- `image:p0004-r3c1` · `regions/p0004-r3c1.png`。m(E)=∞、两球差 A_k，到 E=∪(A_k∩E)，最后‘需要用局部有限性’可供对照。
- `image:p0004-r3c2` · `regions/p0004-r3c2.png`。上部仅第二个球的 k−1 末迹，主要补出 A_k∩E 上‘找每个闭集’，下端空白。

## p0005

`image:p0005` · `pages/p0005.png`。上方 Lusin 逆定理提示，紧接正规、Tietze、Urysohn 的三个条件。中间 Remark 达纸右缘，C=A∪B 独占下一行。下方主定理三条至连续函数列 a.e. 收敛。

- `image:p0005-r1c1` · `regions/p0005-r1c1.png`。从‘Lusin 逆定理也成立’到 (X,τ) 等价、X 正规、闭 E⊂X 与 f∈C(E)。
- `image:p0005-r1c2` · `regions/p0005-r1c2.png`。‘是等价’句右半到 ∃F∈C(X)、F|E=f，顶部余白。
- `image:p0005-r2c1` · `regions/p0005-r2c1.png`。接 Tietze、闭 A,B 不交，Urysohn 端条件之间的 B 状独立字，再到 Remark‘外测度中不对’和单列 C=A∪B。
- `image:p0005-r2c2` · `regions/p0005-r2c2.png`。接 Tietze 结论和 Urysohn 的右括弧，0 与 1 端值看见；Remark 的 m*(A∪B) 后两字近‘除非’，末‘分’抵右缘。
- `image:p0005-r3c1` · `regions/p0005-r3c1.png`。Th. 的 E 上几乎处处有限起句，(1) 可测，(2) φ_k∈S(E) 与分行逐点，(3) φ_k∈C(R^n)。
- `image:p0005-r3c2` · `regions/p0005-r3c2.png`。条件行右端 E∈M 与 (3) 带 a.e. 的箭头至 f；两之间留白。

## p0006

`image:p0006` · `pages/p0006.png`。(1)⇒(3) 的连续延拓、1/2^k、Borel–Cantelli 和最终相等。左缘另有截字，考察可读；全页其余右侧及底部大面积空。

- `image:p0006-r1c1` · `regions/p0006-r1c1.png`。(1)⇒(3)，g∈C(R^n)，下排 k∈N 的角标形短横与竖，取闭 F_k，底部 m(E\F_k)<1/2^k。
- `image:p0006-r1c2` · `regions/p0006-r1c2.png`。延拓的两处限制等式构成重叠区，第二处函数字母 g 后未直接再写 k，F_k 有 k。
- `image:p0006-r2c1` · `regions/p0006-r2c1.png`。从测度小于几何项到 Borel–Cantelli，抽象 limsup E_n，随后可读‘考察’和实际偏差集 E[g_k≠f]，左边字被物理裁切，E\F_k 后有多一右括痕。
- `image:p0006-r2c2` · `regions/p0006-r2c2.png`。仅重露 F_k 后的右括弧、代入 limsup 的 =0 及显式展开的 0 上沿。
- `image:p0006-r3c1` · `regions/p0006-r3c1.png`。偏差集的外交内并，内 ∪ 上方空，接‘几乎任意’的外并内交，两上标 ∞ 可辨，末行 ∃N(x)。
- `image:p0006-r3c2` · `regions/p0006-r3c2.png`。显式展开的 =0、最终相等集合的闭括，最后 f=g_k 恒等；其后无其他证明方向。

## p0007

`image:p0007` · `pages/p0007.png`。第七页整图白底，四边和中部均无笔画、字、页码或续接。

- `image:p0007-r1c1` · `regions/p0007-r1c1.png`。左上全白，纸角与重叠带无字。
- `image:p0007-r1c2` · `regions/p0007-r1c2.png`。右上白边，未见标题、页码或断字。
- `image:p0007-r2c1` · `regions/p0007-r2c1.png`。左中无墨，无左缘裁切字。
- `image:p0007-r2c2` · `regions/p0007-r2c2.png`。右中及其与中左相接的白带均无墨。
- `image:p0007-r3c1` · `regions/p0007-r3c1.png`。左下无正文、脚注或底角签名。
- `image:p0007-r3c2` · `regions/p0007-r3c2.png`。右下全白，结尾无页码和附记。

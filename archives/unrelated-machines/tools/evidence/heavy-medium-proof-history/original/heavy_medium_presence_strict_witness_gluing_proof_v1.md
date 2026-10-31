# 严格双见证下重端与中端占位胶合：作者证明 v1

对应冻结 Exact：`heavy_medium_presence_strict_witness_gluing_exact_v1.md`，SHA256 `f9dad0a0f70f272446042091e0bb400c7a87c6a3f96bae512cfbed34c230183e`。本文件只给限定模板的证明，不向未完成 Exact-first 重构的审查者先发。

下文仅使用每枚 job 的两个已知见证端；未用端点的处理时间完全无关。记

    B = 3/2+(ε+a)/2。

由 ε+a<1，有 B<2。

## 1. 两份 heavy 匹配及其分量

在 job—machine 二部图中，取 σt 的所有 heavy 执行边组成 Nt，t∈{0,1}。每个 job 至多有一条该色边；每台机器至多有一条该色边，因为两个 heavy 的总时间至少 2(1−ε)T>T。因此 Nt 均为真实匹配。共同边先固定；其它并图度至多2，分解成交替路径或交替偶环。

分量的完整方向选择如下。

* machine—machine 路：两个端机分别只在颜色0、颜色1接 heavy；内部机器两方向都接一枚 heavy。选整路的某个颜色即可，无 job 遗漏。
* job—job 路：两个端 job 分别只在颜色0、颜色1走 heavy。选择某色匹配后，恰一个端 job 未匹配，把它放该色原见证的 medium 端；另一个端 job 与内部 jobs 均按该色 heavy 匹配。
* job—machine 路：一色在两个端都多一条边，称其 active 方向。active 时端 job 走 heavy、端机接 heavy；inactive 时端 job 放另一见证的 medium 端、端机不接 heavy。内部机器始终一枚 heavy。
* 偶环、共同边：两方向都在同一机器集合放一枚 heavy，任选方向即可。

这只是对原 jobs 的分配编码，没有新增执行任务。每个 job 的 medium 备选端都由它在未走 heavy 的那份原见证实际给出。

v、w 均在 σ0 heavy-vacant、σ1 heavy-present，所以各自都是并图的一个 machine 端点，绝非内部机器。两者也不属于同一分量：machine—machine 路两端的变化方向相反，而 job—machine 路只有一个 machine 端点。

00、11 直接返回 σ0、σ1。只需证明 mixed。重命名两个测量机后，设所需为 v0、w1。

## 2. v 位于 job—machine 分量时的单分量翻转

从完整 σ1 出发，把 v 所在分量整体由 active 方向翻为 inactive。v 失去 heavy，w 不在该分量而仍有 heavy。内部原机器仍恰一枚 heavy，其所执行 job 的 heavy 时间可能变化，但两个时间都在 [(1−ε)T,T]，因此该机 heavy 负荷最多增加 εT。

此外只有该路径端点的一枚原 job 从 heavy 改为其 σ0 medium 端，成本最多 aT。它的 medium 目的机器允许与发生 heavy 身份变化的机器相同，故不能漏掉两项叠加。所有机器同时满足

    Cmax ≤ (1+ε+a)T ≤ BT，

最后一步因为 ε+a<1。该翻转保留其它全部原任务分配，完整性与合法性直接来自分量的匹配方向及原 medium 端。

## 3. 其余情况的 heavy 方向与真实 medium items

现在 v 在 machine—machine 路上。将其分量选颜色0；w 的不同分量若为 machine—machine 则选颜色1，若为 job—machine 则选 active。其余 machine—machine 路及偶环可任取方向。所有 job—machine 分量一律选 active，故这类端 job 全部走 heavy，不新增固定 medium 负荷。

job—job 分量的方向暂留待 medium 选择。剩余 medium 选择可编码为至多两个选项的 items：

1. 两见证都走 medium 的每枚原 job：两个选项是其 σ0、σ1 原端及相应真实处理时间。
2. 每条 job—job 路：一个 virtual item 的两个选项，分别为两方向留下的两个端点原 job 的已知 medium 端和各自真实时间。选该选项即确定整条路径方向，并只执行相应那个端点原 job 于 medium；另一端点 job 走 heavy。

每个选项成本≤aT，两个成本不要求相等，两个机器也可能相同。virtual item 仅表示一个有限选择，不作为新增执行任务。

将每个 item 的两选项各取一半。记机器 i 的相应 medium 分数负荷为 μ_i，原两见证 medium 实际负荷为 l_i^0,l_i^1。两见证都 medium 的 jobs 和 job—job 端点恰贡献其 half 平均；所有 job—machine 分量 active 只删除原 inactive 见证的一半非负 medium 负荷。因此

    μ_i ≤ (l_i^0+l_i^1)/2。                         (1)

## 4. 两选择不等成本的半积分加权舍入

对任意上述 items，存在一次共同整数选择，使每机器实际所选 medium 总成本≤μ_i+aT/2。

证明：单选项先固定。若一个 item 两个选项在同一机器，选其中成本较小的一个；其负荷不超过原 half 平均。其余 item 的两个 incidences 在不同机器。逐机器将剩余 incidences 按真实成本非增排序，依次将相邻两个配为机器对，至多一个未配。另将每个 item 的两个 incidences 连为 job 对。

由机器对与 job 对组成的多重图，每顶点恰有一条 job 对边、至多一条机器对边，因此分量为路径或边类型交替的偶环。二着色使每个 job 对和机器对均一红一蓝，选择红 incidences。每 item 恰选一个合法原选项。

某机器的成本列表为 c1≥c2≥…≥cs≥0。每机器对恰选一个，其相对 half 平均的总偏差至多

    (c1−c2+c3−c4+…)/2 ≤ c1/2 ≤ aT/2。

奇数末项按正项计；由 c2≥c3、c4≥c5 等逐项比较得中间不等式。已经固定的 items 只使原 half 平均下降。所有机器同时由同一个二着色选择满足此界。

按每个 virtual item 的选择恢复其 job—job 匹配方向，其它原 medium jobs 放所选端。至此全部原 jobs 恰执行一次，heavy-presence 的两个测量值已由先前的 machine 端点分量确定，virtual 方向不改变它们。

## 5. 逐台原机器的完整负荷

两原见证严格≤T，故有 heavy 的见证在该机的 medium 负荷≤εT，无 heavy 的见证 medium 负荷≤T。

* 两见证均 heavy-present：由(1)及舍入，medium 负荷≤εT+aT/2。最终只有一枚 heavy，时间≤T，总负荷≤(1+ε+a/2)T≤BT；最后使用 ε≤1。
* 两见证的 heavy-presence 不同：medium 均值≤(1+ε)T/2；舍入后再加最终至多 T 的 heavy，负荷≤[3/2+(ε+a)/2]T=BT。若最终无 heavy 只会更低。
* 两见证均 heavy-vacant：其并匹配没有 heavy 边，构造不会让它新增 heavy。medium 负荷≤T+aT/2≤BT。

此三类覆盖全部机器；并非仅核 v,w。配合第2节，得到两种 mixed 模式，00、11 已由原见证给出。

## 6. 复杂度、退化与范围

只保留各 job 的至多两个见证端。构造两匹配并分解、建立 items、逐机器排序及路径/偶环二染色、再恢复原 job 分配，运算次数为显式输入规模的多项式。中间负荷都是输入有理数的部分和，分母位长不超过相关输入分母位长总和；排序比较亦可精确完成。没有按 1/a、1/ε 或 1/(1−ε−a) 的数值迭代。

a=0 时所有 medium 成本为零，同一舍入与恢复仍合法；ε=0 时 heavy 均为 T，单分量翻转的 εT 项为零。两个 medium 端在同一机器但成本不同，可按第4节选较小者并据其 virtual 选择恢复方向。σ0=σ1 的原 job 保留原端；共同 heavy 边固定，不会被错误重复执行。

结论只测两机器是否实际接到 heavy 原任务，不保产生该占位的具体 job 身份或其它外部边界。所用端点 gap 外的角色、多机器同时锁定与原源标签解码并未由此证明。本候选仅给严格双见证下 cross-role presence 复制合同的一个统一低于2边界，未声称全参数锐性或一般 UM 算法。

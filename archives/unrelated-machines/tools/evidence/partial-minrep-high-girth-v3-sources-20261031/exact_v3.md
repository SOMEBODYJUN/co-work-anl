# 正规高围长部分MinRep源：v3精确陈述先行

精确身份：`UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3`。本候选扩展既存v2线性degree源；对象和算法不同，另立版本。本文只给精确陈述和算法，不含概率证明。

固定整数G≥2（不把binary G变参数时的指数隐藏成poly）。输入为显式无权平衡D-regular二部全投影游戏Π，两侧各n≥1点，N=2n，原D≥1，可有平行约束且作为独立edge types计数。共同Σ大小Q≥2，每条投影表显式。参数binary整数g≥2、有理0<rho≤1，且Q gamma≥1，其中

ell=floor(log2 g), lambda=1+ceil(log2 Q), tau=rho/(100g²), gamma=rho³/(10^9g⁸), d=ceil(1000g lambda/(rho ell)).

最后一个Q gamma≥1是显式域条件，保证参数数值可按显式Q输入界控制；若Q gamma<1，val(Π)≤gamma在非空全投影域本就不可能。列表可空，cost为全部顶点列表大小之和，covered iff有兼容标签对。

定义S=Σ_(l=2..G)d^l，B=40NS，U=Σ_(j=0..G+1)d^j，m_*=dN/2。取

z=ceil max{2G+1, G B+4U+1, 8B/(rho m_*)}, t=D z。

## 明确算法

建立原每顶点t份copies。先做一个canonical template perfect matching：每个原顶点按其D个incident edge types把自己的t个slots等分成D组，各z个；每条原edge type把对应两组slots按局部index一一匹配。因此template本身是全部左/右copy slots之间的perfect matching，恰每个原type有z条边。

独立做d个layers。每layer、每原顶点各抽一份uniform [t] permutation，将此点template slots重命名到t个copy编号；template沿原edge type继承其原projection。d个layers的union（保留layer/type标记）是d-regular平衡multigraph，顶点数N′=Nt、边数M′=t m_*。

抽uniform permutation用Fisher–Yates；每个uniform整数draw用ceil(log2 bound) fair bits拒绝采样，至多R=ceil(log2(2000dN(t−1)))次，任一耗尽即返回FAIL。因此随机位和最坏时间有有限硬上界；所有draw成功条件下permutations仍独立uniform。

枚举长度2..G的所有simple cycles，parallel edges算2-cycle；若数量X>B返回FAIL。否则反复选一个长度≤G cycle的一条边e，在同一(original edge type,layer) bucket找另一edge f：f不在任何当前长度≤G的cycle，且其两端均离e两端的图距离>G（当前底层undirected multigraph）。若e=(u,a)(v,b)、f=(u,c)(v,d)，则替换为(u,a)(v,d)、(u,c)(v,b)，原layer/type/projection均继承，继续到无短cycle。本文声称这个f总能找到。

## 精确结论

1. 对每个seed，算法只返回FAIL或一个显式平衡、simple、d-regular、girth>G、字母表不变的游戏，所有剩余/新边继承某个原edge type投影。所有root copies等同使用原labels时，原perfect满足赋值满足输出全部边。
2. 对全部合法输入，返回FAIL的概率<0.1。若val(Π)=1，每个非FAIL输出都perfect-complete；调用者可将FAIL分支直接作为YES/empty-jobs UM实例处理，不对它伪造girth游戏。
3. 若val(Π)≤gamma，以至少0.8概率算法返回非FAIL输出，且每个cost≤gN′的多标签赋值均覆盖严格少于rho M′。量词同时覆盖全部copy lists，并允许同一原顶点的copies使用完全不同的lists。
4. 对固定G，算法的最坏时间、输出规模及随机位总数关于全部显式原图/投影表及binary g,rho为多项式；指数可依G。没有按2^G隐式处理图，也没用无限拒绝采样。域Q gamma≥1对uniform复杂度有实际用途。
5. 若PCP起点先固定g,rho，保持Q=poly_rho(g)，则d=O_rho(g)，并能同时要求任意先固定girth>G；这只是一个源桥，不是UM compiler。随机归约反证仍采用NP不包含BPP，而非直接P≠NP。

## 范围、依赖与状态

声称的证明须同时核cheap copy-list平均覆盖、两侧fiber permutations的高阶同时性、短cycle期望、same-type/layer switch可选性和不生短cycle、所有lists的统一repair误差、bounded-bit FAIL概率和总位复杂度。单标签Azuma不足以自动证明第3项。

无已实现软件/有限实验声明；没有把随机高girth源当任意lift都保soundness，更没有从它推出near2 UM困难性。配置有限cover整数化障碍仍成立；本稿仅可能选到soundness保持的随机连线。root已有候选证明，应先由审查者只据此Exact独立重构，再读冻结证明攻击。

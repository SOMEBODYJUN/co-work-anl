# 七极大、六提供者：至多两个全局私有极大集的半覆盖证书

**状态：条件性精确证书，内部 Fraction 核验；不是 unrestricted Q-CAG-HALF-6 的闭合。**

## Exact statement

在原 CAG 模型中，恰六名提供者、全部有序历史纯 SPE。设共同目录恰有七个 distinct inclusion-maximal coverage sets `B_0,...,B_6`。若至多两个最大集有非空 singleton-incidence block（存在客户只属于该最大集），则

`OPT_6 = U <= 2W`, `U=|B_0∪...∪B_6|`.

因此该结构类满足六人半覆盖。内部子主题、重复、空主题、零客户和历史依赖平局保留。若三个或更多最大集有 singleton block，本行族不闭合；这不是反例。

至多两个 singleton block 意味着至少五个最大集无 singleton 客户。选一个无 singleton block 的最大集作为六主题最优组合省略的 `B_6`，所以 `OPT_6=U`。将真实最终最大动作重标成 `B_0`；若两个 singleton block 中含 `B_0`，属于“含最终集”轨道，否则属于“不含最终集”轨道。`B_1,...,B_5` 的置换只产生这两类。

## Valid rows

最后行动者在每个合法前缀选择 inclusion-maximal coverage。设 `I` 为客户的 maximal-incidence 集，`E⊆{0,...,4}` 为实际前五动作成员位，则最终位满足 `1_{5∈J}=1_{0∈I}`。用 `dynamic_maxima_bound.md` 的 mixed-floor：对 `t=0,1,2,3`

`u_t >= c/6 + P A_t + V b_t >= b_t U`,

其中 `b=(1/21,2/37,1/16,2/27,1/11,7/72)`，且 `A_t>=b_t`、`1/6>=b_t`。因此真实非负行 `M_t=u_t-b_tU` 可用于所有 singleton 类型；证书只用 `M_0,...,M_3`。另用：

- 末位对每个 `B_j` 的真实 best-response 行 `L_j`；
- 实际前缀末两位对每个 `(B_j,B_k)` 的 genuine two-remaining tax 行 `T_{jk}`。

这些行都来自完整原策略的真实历史，不合并计数历史，也不把 SPE 改成静态 NE。逐客户求和的精确残差证明 `W-U/2>=0`。

## Exact multipliers

行顺序为 `M0..M5,L0..L6,T00,T01,...,T66`，`T` 按 `combinations_with_replacement(range(7),2)`。

### 含真实最终集的两个 singleton 轨道：`I={0}`, `I={1}`

非零乘子：

- `M0=M1=M2=M3=133/207`；
- `L1=4/23`，`L2=L3=L4=L5=L6=2/23`；
- `T01=31/207, T02=19/207, T03=4/69, T04=T05=T06=19/207, T13=7/207`。

允许全部 `|I|>=2`，以及 singleton `I={0},{1}`。3904 个类型列的最小残差为 `34955/3308688`，在 `(I,E,J)=(1,0,32)`。

### 不含真实最终集的两个 singleton 轨道：`I={1}`, `I={2}`

非零乘子：

- `M0=416/635, M1=833/1270, M2=167/254, M3=84/127`；
- `L1=10/127`, `L2=L3=L4=L5=L6=16/127`；
- `T01=T02=25/127`；
- `T03=T04=T05=T06=T13=T14=T15=T26=3/127`。

允许全部 `|I|>=2`，以及 singleton `I={1},{2}`。3904 列最小残差为 `30253/9473184`，在 `(I,E,J)=(2,0,0)`。

The complete rational residual is checked by the standalone script. Since the omitted maximum has no singleton customers, every type—including any singleton type—belongs to `U=OPT_6`; the target coefficient is `1_{J≠∅}-1/2`.

## Verification

From repository root:

```sh
python3 research/workspaces/customer-attraction/R-41809d4a3a4a4ad49d9054cab81df358/singleton_two_maxima/audit_singleton_two_maxima.py
```

Expected:

```text
with_final {'columns': 3904, 'minimum': '34955/3308688', 'arg': (1, 0, 32)}
without_final {'columns': 3904, 'minimum': '30253/9473184', 'arg': (2, 0, 0)}
```

This is an exact coefficient certificate for the stated incidence subclass, not a finite search, target counterexample, or unrestricted six-person proof.

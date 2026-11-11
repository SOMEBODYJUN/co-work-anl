"""A real source-5 deviation pays a new universal source-2 maximum-C row."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

P = Path(__file__).resolve().parent
W = P.parent
REPO = W.parents[2]


def dump(name, obj):
    path = P/name
    assert not path.exists(), 'Preserve this frozen derivation; make a versioned successor.'
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def main():
    assert not (P/'manifest.json').exists()
    theta = F(5,12)
    states, minima, critical = [], [], []
    for p,c,o in product(range(2),repeat=3):
        m0 = F(5*c,2)+F(24*c,p+5)+F(o,6*(p+1+4*c))
        slope = F(o,6*(p+3*c+2))-F(c,5)
        expected = m0+theta*slope
        values, zeros = [], []
        for rr in product(range(2),repeat=4):
            r3,r4,r5,r6 = rr
            L = p+c+sum(rr)
            def share(num):
                assert L or num == 0
                return F(num,L) if L else F(0)
            base = share(25*c-r6)+F(sum(rr[:3]),2)+r6+F(o,6*(p+c+sum(rr[:3])+1))
            increment = F(o,6*(p+c+r3+r4+2))-share(r5)
            cost = base+theta*increment
            assert base >= m0 and cost >= expected
            residual = cost-expected
            states.append(dict(p=p,c=c,o=o,r=list(rr),base=str(base),increment=str(increment),
                               cost=str(cost),minimum=str(expected),residual=str(residual)))
            values.append(cost)
            if not residual:
                zeros.append(list(rr))
            if increment < slope:
                critical.append(((base-m0)/(slope-increment),(p,c,o),rr))
        assert min(values) == expected
        minima.append(dict(p=p,c=c,o=o,m0=str(m0),slope=str(slope),minimum=str(expected),zero_states=zeros))
    assert len(states) == 128 and min(item[0] for item in critical) == theta
    # Literal six-query multiplicity, before the union projection.
    literal_checks = 0
    for p,c in product(range(2),repeat=2):
        for rr in product(range(2),repeat=4):
            r3,r4,r5,r6 = rr
            for q in product(range(2),repeat=6):
                d,o = sum(q),int(any(q))
                D6 = p+c+r3+r4+r5+1
                D5 = p+c+r3+r4+2
                actual = sum((F(v,D6)+theta*F(v,D5) for v in q),F(0))/6
                projected = F(o,6*D6)+theta*F(o,6*D5)
                assert actual-projected == F(d-o,6)*(F(1,D6)+theta*F(1,D5)) >= 0
                literal_checks += 1
    row = dict(name='SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE',family='TRUE_SAME_BRANCH_NESTED_SAFE',
               rhs='0',numerical_divisor='300',a={})
    for idx in range(512):
        bits = [(idx>>k)&1 for k in range(8,-1,-1)]
        a,x,o,c = bits[:6],bits[6],bits[7],bits[8]
        p,total = a[0],sum(a)
        u2 = F(a[1],total) if total else F(0)
        B,M,N = F(c,p+5),F(o,6*(p+4*c+1)),F(o,6*(p+3*c+2))
        value = 300*u2-288*B-12*M-5*N
        row['a'][str(idx)] = str(value)
        expected = F(5*c,2)+24*B+M+theta*(N-F(c,5))
        # The |C|=K equality is used only after the complete real-source payment.
        assert 12*(25*u2-expected)+29*c == value
    row['a']['512'] = '1'
    dump('hidden_state_checks.json',states)
    dump('minimum_table.json',minima)
    dump('SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json',row)
    proof = r'''# 最大 C 的第二源分支：把内部第五源偏离接回定量覆盖预算

Boss1 / RUN six-boss1-20261111。Main 直接推导；0 次优化器。

## 普遍结论

有限单位客户、有限非空共同标签目录、恰六人、任意完整有序历史纯 SPE。
令 A1 为实际首标签，u2 为实际第二人收益，C 为真正达到最大裸大小 K
的合法标签；任取六个合法查询 Q1,…,Q6（允许重复）及其覆盖并 O。
逐客户记 p=1[A1]、c=1[C]、o=1[O]，定义

\[
B=\sum_x\frac{c_x}{p_x+5},\qquad
M=\sum_x\frac{o_x}{6(p_x+4c_x+1)},\qquad
N=\sum_x\frac{o_x}{6(p_x+3c_x+2)}.
\]

则有新的普遍必要付款

\[
\boxed{300u_2+K\ \ge\ 288B+12M+5N.}
\tag{NS5}
\]

这不是仅在旧 P25 取等时才成立的条件关系。O 只表示六个真实查询的并，
不必最优、不须是合法行动。C 与任何实际标签或查询可以相同、覆盖相同
而标签不同，也可完全不同；所有弱平局、空主题、重复行动和零客户保留。

## 同一个真实偏离分支的完整付款

在实际第二源历史 (A1) 强制合法 C，沿给定同一完整策略取真实
R3,R4,R5,R6，逐客户会员为 r3,r4,r5,r6，负载
L=p+c+r3+r4+r5+r6。v2,…,v6 始终指这一条分支的真实终局收益。
使用如下非负预算：

| 真预算 | 权 |
|---|---:|
| 第二源 IC：u2−v2 | 25 |
| K−|R3|、K−|R4|、K−|R5| | 各 1/2 |
| K−|R6| | 1 |
| 同一末节点对六个 Qj 的 BR 平均 | 1 |
| 该真实第五源对六个 Qj 的 SAFE 平均 | 5/12 |

末节点的前缀是 (A1,C,R3,R4,R5)，直接 BR 成本为
d/[6(p+c+r3+r4+r5+1)]，其中 d=Σj 1[Qj]。
内部第五源的前缀是 (A1,C,R3,R4)。对每个 Qj 强制偏离后，
只用它自己的真实末回复；该回复最多使每个 Qj 客户再加一负载，
所以 SAFE 成本为 d/[6(p+c+r3+r4+2)]。
该源本身实际选择 R5，故收益付款是同一 v5，绝不替换为 u2 或实际 u5。
这些源收益在后面的逐客户投影中才被消去。

加权和逐客户的准确成本，在以 d≥o 弱化两个正菜单成本后为

\[
\begin{aligned}
\Psi(p,c,o;r)={}&
\frac{25c-r_6-(5/12)r_5}{L}
+\frac{r_3+r_4+r_5}{2}+r_6\\
&+\frac{o}{6(p+c+r_3+r_4+r_5+1)}
+\frac{5o}{72(p+c+r_3+r_4+2)}.
\end{aligned}
\tag{COST}
\]

零负载时第一项分子亦为零，按零处理。因此

\[
25u_2+\frac52K-\sum_x\Psi(p_x,c_x,o_x;r_x)\ge0.
\tag{PAY}
\]

更准确地，(PAY) 的左端是表中七项真预算，加上
(d−o)[1/D6+(5/12)/D5]/6 的逐客户非负菜单余项。
两个均值都来自同六个真实合法查询；没有采用相互独立的客户边际。

## 全隐藏域的精确最小值

p,c,o 各为0或1，四个真实尾会员各为0或1，共128个完整状态。
令

\[
m_0=\frac52c+\frac{24c}{p+5}+\frac{o}{6(p+4c+1)}.
\]

完整逐客户最小值为

\[
\min_{r\in\{0,1\}^4}\Psi
=m_0+\frac5{12}\left(\frac{o}{6(p+3c+2)}-\frac c5\right).
\tag{MIN}
\]

下面表与 hidden_state_checks.json 中全部128个有理余项共同给有限域
精确证明；build_exact.py 直接按真份额重建每项，不使用优化器。
同时对全部4096个真实六查询会员情形核验 d 到 o 的准确非负差。
表中四位依次是 r3,r4,r5,r6。

TABLE

保留 p=1,c=1 时末位可以不覆盖 C 的弱平局。新公式并不要求四尾
全部等于 C，也没有把同覆盖标签的有序历史当成同一个历史。
系数 θ 在 [0,5/12] 内时，MIN 对应的仿射式由两个端点余项均非负
而成立。该简单仿射式不能继续超过5/12：状态
(p,c,o;r)=(0,0,1;0,0,1,0) 在5/12处达到零余项，之后变负。
这只说明当前闭式段的端点，不声称所有可能真预算的最优权。

## 消去真实 C 质量得到新行

把 (MIN) 代入 (PAY)，再用准确的 Σc=|C|=K，并乘12：

\[
\begin{aligned}
12\left[25u_2+\frac52K-\sum_x\min_r\Psi\right]
&=300u_2+30K-[30K+288B+12M+5N-K]\\
&=300u_2+K-288B-12M-5N\ge0.
\end{aligned}
\]

这证明 (NS5)。所保存的新行使用全部512个 (a1,…,a6,x,o,c) 类型
和独立 K 列；x 位完全保留但本行不使用它。该行按上述整数尺度保存，
供未来数值使用的正除数为300。不得在已冻结1002行输入中悄悄加入它。

## 对当前未付义务的作用

旧真实 P25(C,Omean) 利用 |C|=K 后为 25u2−24B−M≥0。
若此预算取等，(NS5) 进一步要求 K≥5N。
它将“同一真实分支的中间后继还必须各自最优”变为有明确支付的全域行，
无需先固定一个低福利点或构建离轨补全 LP。
原六人 half 仍开放；本包仅证明新增必要关系，未认领任何新的全局锥最优值。
'''
    table = '| p | c | o | 精确最小值 | 达到的尾状态 |\n|---:|---:|---:|---:|---|\n'
    for r in minima:
        table += '| '+ ' | '.join([str(r[k]) for k in ['p','c','o','minimum']]+[', '.join(''.join(map(str,z)) for z in r['zero_states'])])+' |\n'
    (P/'proof.md').write_text(proof.replace('TABLE',table))
    cert = dict(status='PASS_MAIN_REAL_SOURCE2_C_WITH_INTERNAL_SOURCE5_SAFE',optimizer_calls=0,
                theta=str(theta),hidden_states=128,minimum_types=8,literal_menu_checks=literal_checks,
                raw_row_count=1,columns=513,parameter_scope='Any six legal query union; actual first history; true globally maximal C.',
                direct_budget_weights=dict(source2_IC='25',CAP_R3='1/2',CAP_R4='1/2',CAP_R5='1/2',CAP_R6='1',terminal_mean_BR='1',internal_source5_mean_SAFE='5/12'),
                critical_affine_endpoint=[dict(p=x[1][0],c=x[1][1],o=x[1][2],r=list(x[2])) for x in critical if x[0]==theta])
    dump('exact_certificate.json',cert)
    sources = []
    for path in ['archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
                 'research/workspaces/six-boss1-20261111/main_all_source25_family/proof.md']:
        sources.append(dict(path=path,sha256=sha256((REPO/path).read_bytes()).hexdigest()))
    artifacts = {f.name:sha256(f.read_bytes()).hexdigest() for f in P.iterdir() if f.is_file()}
    dump('manifest.json',dict(status='FROZEN_MAIN_PROOF_AND_COMPLETE_FINITE_RESIDUALS',sources=sources,
                              artifacts=artifacts,optimizer_calls=0))
    print(json.dumps(cert,ensure_ascii=False))


if __name__ == '__main__':
    main()

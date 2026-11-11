"""Append the exact all-type tail-wallet certificate to the new formal root owner."""
from pathlib import Path
from fractions import Fraction as F
import json

HERE=Path(__file__).resolve().parent;WS=HERE.parent;REPO=WS.parents[2]
BODY=REPO/'archives/customer-attraction/state/引理/最大主题真实尾部的根收益加强--引理.md'

def main():
    text=BODY.read_text();assert '## 8. 真第三' not in text
    d=json.loads((WS/'main_maximal_root_tail_check.json').read_text());assert d['status']=='PASS'
    assert d['certificate_sha256']=='80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771'
    header=r'''

## 8. 真第三、四、六源和完整末两位的另一条根界

仍在同一真实根C分支(C,B2,B3,B4,B5,Z)上，定义v_j为该分支第j人最终收益，v1=v、v5=s、v6=w；l=(p,y2,y3,y4,y5,z)，c为六位之和。令

\[
S_j=v_j-\sum\frac{o}{6(\sum_{k<j}l_k+7-j)}\ge0,
\qquad j=3,4,6.
\]

这些都是各自真实有序前缀下的六合法查询SAFE，不能用实际路径收益替换。末两人真实背景D=p+y2+y3+y4+1的配对平均预算为

\[
P_{OO}=v_5+v_6+\sum\frac{y_5}{D(D+1)}
-\sum\left[\frac{o}{3D}-\frac{o}{36D(D+1)}\right]\ge0.
\]

对每个合法Q,R，PAIR由第五源改Q的IC、其同一个真实末回复对R的BR、原末节点对该回复的BR，再加逐客户非负自交差支付。将六查询的全部36个有序对平均，真实重数d给d/(3D)−d²/[36D(D+1)]。当1≤d≤6时，减去并指标o=1的值为(d−1)[12(D+1)−(d+1)]/[36D(D+1)]≥0。因此P_OO确由真实36对付款，未把并集当行动、未作独立性假设。

下表是十个非负预算的整数权。N=112944305160。

| 预算 | 整数权 |
|---|---:|
| I=u−v1 | 112944305160 |
| D2=K−\|B2\| | 939131055 |
| D3=K−\|B3\| | 6218848680 |
| D4=K−\|B4\| | 6200167680 |
| D5=K−\|B5\| | 6031687680 |
| DZ=K−\|Z\| | 6390005760 |
| S3 | 5324085000 |
| S4 | 5380128000 |
| S6 | 2508226560 |
| P_OO | 3881779200 |

记五个大小权依次为C2,...,C6，末四个查询权为s3,s4,s6,t。逐客户定义

\[
r(l,o)=N\frac{p}{c}+\sum_{j=2}^{6}C_jl_j
-37375524862p-2178783435o
-s_3S_3(l,o)-s_4S_4(l,o)-s_6S_6(l,o)-tP_{OO}(l,o),
\]

其中S_j(l,o)、P_OO(l,o)指上面预算的逐客户系数，零份额按之前约定。完整128型的r如下：

| p,y2,y3,y4,y5,z | r(o=0) | r(o=1) |
|---|---:|---:|
'''
    rows=[];rr=d['residuals'];assert len(rr)==128
    for j in range(0,128,2):
        a,b=rr[j],rr[j+1]
        assert a['bits'][:-1]==b['bits'][:-1] and a['bits'][-1]==0 and b['bits'][-1]==1
        v,w=F(a['integer_scaled_residual']),F(b['integer_scaled_residual'])
        assert v.denominator==w.denominator==1 and min(v,w)>=0
        rows.append('| '+''.join(map(str,a['bits'][:-1]))+' | '+str(v)+' | '+str(w)+' |')
    footer=r'''

全部128型中115个正、13个零。五个大小权之和为25779840855，而37375524862−25779840855=11595684007。用K=Σp、O=Σo消去两个自由质量等式，得到精确非负恒等式

\[
112944305160u-11595684007K-2178783435O
=NI+\sum_{j=2}^{6}C_jD_j+s_3S_3+s_4S_4+s_6S_6+tP_{OO}+\sum r(l,o)\mu_{l,o}\ge0.
\]

此即TAIL。没有使用分支覆盖≤O或u≥K/6的预算，故O可为任意六合法标签覆盖并。工作中的71行必要LP为保证它是OPT6的投影另保这两个约束，但其对偶权均0；不能把整份LP的适用域与本正权恒等式混淆。

取K0=24376964954228547006/142891298915142483961、O=1时，71行/129列必要系统有匹配精确原始点u*=197998925913631121419767306359/5379586156460209884457196512920。这只证明这个指定必要锥在K0的最优性，不证明TAIL为原SPE锐界。全部9159系数、71原始行、129对偶列和独立K/O两列分别由builder外的标准库checker及独立审计核过；Main又独立重建上述十预算的128个r和两个自由乘子。

完整材料在research/workspaces/six-boss1-20261111/maximal_root_tail_wallet/、maximal_root_tail_audit/及main_maximal_root_tail_check.py/.json；所有旧冻结来源字节保持。原六人半覆盖仍未由这些根界闭合。
'''
    BODY.write_text(text+header+'\n'.join(rows)+'\n'+footer)
    print('appended exact128type certificate')

if __name__=='__main__':main()

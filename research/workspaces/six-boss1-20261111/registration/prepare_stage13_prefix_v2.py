"""Main serial promotion of the uniform dual and unique optimal weights."""
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
PREFIX='research/workspaces/six-boss1-20261111/'
OID='customer-attraction/shared-maximal-potential-early-safe-prefix-family'
BODY='archives/customer-attraction/state/引理/共同最大潜力主题的早期安全预算投影--引理.md'
def bind(p):
    return {'path':p,'sha256':sha256((REPO/p).read_bytes()).hexdigest()}

def main():
    raw=(REPO/'research/registry.json').read_bytes()
    reg=json.loads(raw)
    obj=next(o for o in reg['objects'] if o['object_id']==OID)
    assert obj['version']==1 and obj['body']==bind(BODY)
    assert obj['body']['sha256']=='bb260d9366608cb076dbd425fd4c625bc40609c3e39e7d048377ec372694eefd'
    text=(REPO/BODY).read_text()
    text=text.replace('status: proved-all-type-early-prefix-necessary-bounds',
                      'status: proved-all-type-bounds-and-unique-optimal-weights',1)
    text=text.replace('  - local:research/workspaces/six-boss1-20261111/early3_maxx_cone/audit_main_family.md',
        '  - local:research/workspaces/six-boss1-20261111/early3_maxx_cone/audit_main_family.md\n'
        '  - local:research/workspaces/six-boss1-20261111/main_prefix_cone_uniform_dual.md\n'
        '  - local:research/workspaces/six-boss1-20261111/prefix_uniform_dual_audit.md',1)
    text=text.replace('第一、第二位此处只声明有效。没有声称这些常数是真实SPE锐界',
                      '前三位的完整指定权锥最优与唯一性现由下一部分证明。没有声称这些常数是真实SPE锐界',1)
    # The original valid-bound proof remains the bearing argument; append the new exact cone result.
    extra=(WS/'main_prefix_cone_uniform_dual.md').read_text()
    extra=extra[extra.index('## 1. 完整锥与记号'):]
    extra=extra.replace('## 1. 完整锥与记号','## 7. 完整非对称预算锥与记号',1)
    extra=extra.replace('## 2. 只需五类原始类型','## 8. 只需五类原始类型',1)
    extra=extra.replace('## 3. 一个对所有原权都成立的恒等式','## 9. 对所有原权成立的统一对偶',1)
    extra=extra.replace('## 4. 完整最优权唯一','## 10. 完整最优权唯一',1)
    extra=extra.replace('## 5. 核验及下一义务','## 11. 独立核查与第三位PAIR直接延伸',1)
    extra=extra.replace('独立审读仍单独保存。','独立审读已经完成，见本RUN的prefix_uniform_dual_audit.md及同名目录。',1)
    text=text.rstrip()+'\n\n'+extra.strip()+'\n'
    text+=r'''
独立审查从原份额重新构造全部1440型，核33088次付款仿射基及305个支撑闭式；
支撑等式加a_T=0的精确秩分别8、10、12，行列式为−1/4320、9/400000、
4/2278125。没有导入或运行Main脚本，不读任何游戏点。

第三位再加三份指定真PAIR时，还有直接七支撑恒等式。明确原第三位强制X后的
三尾为Y、Z、T，真实倒二前缀是(h2,X,Y)，背景d=b+x+y+1=n+x+y。
对合法L,R，写U(L,R)=Σl/(d+r)、f(L)=Σl/d、g(L,R)=Σlr/[d(d+1)]。
其真实两尾收益为u'=U(Z,T)、v'=U(T,Z)，则

\[
TP(L,R)=u'+v'+g(Z,Z)-f(L)-f(R)+g(L,R)\ge0.
\]

令J_L为同一倒二前缀真改L后的σ末回复，准确付款为

\[
\begin{aligned}
TP(L,R)={}&[u'-U(L,J_L)]
+[U(J_L,L)-U(R,L)]\\
&+[v'-U(J_L,Z)]+[g(Z,Z)-g(Z,J_L)].
\end{aligned}
\]

前三项是三个真实节点的IC，末项逐客户非负。只增加
TP(Q,X)、TP(Q,Q)、TP(X,X)，给全局非负权η1、η2、η3。
令E^pair为(E)再减三份逐客户TP系数，则

\[
\begin{aligned}
C-\frac{61}{3}
={}&\frac{38}{3}E_A^{pair}+\frac{52}{3}E_G^{pair}
+20E_H^{pair}
+2(E_{B_1}^{pair}+E_{B_2}^{pair})\\
&+6(E_{D_1}^{pair}+E_{D_2}^{pair})
+\frac89a_T+6\eta_1+\frac13\eta_2+\frac{139}{6}\eta_3 .
\end{aligned}
\]

全部剩余系数严格正。因此十一权最优仍为61/3，且唯一向量为
(15,2/3,2/3,4,1,1,0,1,0,0,0)。这组七支撑加四个零坐标的等式矩阵
精确秩11；独立核验也保留了全部160份真实PAIR付款和864项逐型系数。
以上仍仅限所列预算锥，不升级为实际SPE锐性或六人half结论。
'''
    (REPO/BODY).write_text(text)
    obj['version']=2
    obj['title']='同一最大潜力标签的早期SAFE/MAX投影及完整权锥唯一最优'
    obj['statement']+=' 三个完整非对称2r权逐型锥分别精确最优61/3、121/4、206/5；统一7/9/11支撑对偶的末MAX正余项ρ=8/9、85/16、18，强制唯一最优权为正文三组参数。第三位再加正确倒二前缀的三份指定PAIR仍唯一为八权最优追加三个零，另有直接七支撑十一列恒等式。'
    obj['scope']+=' 完整非对称2r非负全局权锥（r=4,5,6）的最优与唯一性；第三位指定三PAIR扩展十一权的最优与唯一性。均给逐系数解析恒等式与非退化唯一方程。'
    obj['quantifiers']+=' 另对r=4,5,6的全部2r个独立非负全局预算权，要求全部原始有序布尔型余项非负而最小化C；第三位十一权扩展仅加正文三份指定PAIR，所有权不按客户变化。'
    obj['objections']=obj['objections'].replace('第一、第二位此版本只证有效，不证最佳；第三位限定八预算锥的最优不等于真实SPE锐性。',
        '前三位及第三位指定PAIR扩展只在明定预算锥中证明唯一最优，不等于真实SPE锐性。')
    obj['body']=bind(BODY)
    extras=[
        'main_prefix_cone_uniform_dual.md','main_prefix_cone_uniform_dual.py',
        'main_prefix_cone_uniform_dual.json','prefix_uniform_dual_audit.md',
        'prefix_uniform_dual_audit/verify_audit.py','prefix_uniform_dual_audit/audit_result.json',
        'prefix_uniform_dual_audit/support_coefficients.json','prefix_uniform_dual_audit/freeze_manifest.json',
        'early3_pair_cone.md','early3_pair_cone/exact_certificate.json',
        'early3_pair_cone/independent_verification.json','early12_safe_maxx_cones.md',
        'early12_safe_maxx_cones/exact_certificate_r5.json','early12_safe_maxx_cones/exact_certificate_r6.json',
        'early12_safe_maxx_cones/independent_verification.json']
    known={e['path'] for e in obj['evidence']}
    obj['evidence'] += [bind(PREFIX+p) for p in extras if PREFIX+p not in known]
    obj['sources']=list(dict.fromkeys(obj['sources']+['material:'+PREFIX+p for p in extras]))
    mats={m['path']:m for m in reg['materials']}
    for e,bodyflag in [(obj['body'],True)]+[(e,False) for e in obj['evidence']]:
        p=e['path']
        if p in mats:
            if mats[p]['sha256']!=e['sha256']:
                assert p==BODY
                mats[p]['sha256']=e['sha256']
        else:
            m=dict(e,disposition='objects' if bodyflag else 'attachment',
                   object_ids=[OID],reason='Main全类型证明、统一稀疏对偶与唯一性，独立真实份额及精确秩核验；限定预算锥。')
            reg['materials'].append(m);mats[p]=m
    target=HERE/'stage13-prefix-v2-registry-candidate.json'
    assert not target.exists()
    target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    (HERE/'stage13-prefix-v2-object.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    summary={'base_registry_sha256':sha256(raw).hexdigest(),'object_id':OID,'version':2,
             'body':obj['body'],'objects':len(reg['objects']),'materials':len(reg['materials'])}
    (HERE/'stage13-prefix-v2-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()


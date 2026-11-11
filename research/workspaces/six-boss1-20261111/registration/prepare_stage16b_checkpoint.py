"""Save the formatting correction and continuing real mathematics before publishing."""
from pathlib import Path
from hashlib import sha256
import gzip
import json
import subprocess

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=HERE.parents[3]
RUN='six-boss1-20261111'

NOTE=r'''# Stage16b 当前恢复入口：正式回流修正、可见 C 精确界及内部真源的新付款

Boss1 / RUN six-boss1-20261111；customer-attraction/six-providers；rebuild/research-v2。
原题2W≥OPT6仍OPEN，Main继续。写本说明时最后确认pushed仍是
18c46242b4b378d43b4beb6f5ed03c41a4819ab3。Stage16第一次checkpoint因两处
相同公式行末空白失败，未提交；实际恢复上限须看后续Stage16b的pushed回执。

## 当前 Main 已亲核的精确普遍界

完整512客户型(a1,…,a6,x,o,c)+K的1002raw/513col/2eq必要锥，唯一一次LP后
精确恢复得到

α=4757095109515738566700794768667543071677 / 10803370013405844497554807694481975324637
≈.44033436822146094，且原模型 W≥α OPT6。

完整input在visible_maximum_joint/，SHA b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33；
完整原对偶、12正付款、最优面及真实分支排除在visible_maximum_joint_solve/，
cert SHA8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347，
manifest13a5a0206c1332433fa823d25be67cb6b1244375c0269c8e9dca7e3aef0dc98f。
Main亲读完整proof并用main_visible_c_certificate_check.py/json另核全部1002原行、
513对偶余项、两等式、互补/目标、21零余项支持上14秩、七参数完整表达、
1002参数化原不等式及6个fixed量有符号身份；没有调用优化器。

整个最优面不能由完整SPE实现。正P25 source2(C,Omean)使三个中间真实后继
覆盖恰C，真实源收益均等于actual u2；p=a1=1时末位1110和1111弱平局均保留。
全脸A1⊆C、A1∩X空、K/|A1|/|X|/u2固定，内部第三源查X需
u2≥|X|/4−(K−|A1|)/20，而固定差为
73001712264841918690793563657687463721 / 108033700134058444975548076944819753246370>0。
这只是等号排除，不能单凭严格不等号声称统一正增量；完整半覆盖仍未证明。

## Main已经补出的定量约束

新冻结包main_source2_maximum_nested_safe/有完整源证明、128态余项、4096真实
菜单核验及513列新行，0优化。实际首标签A1会员p∈{0,1}，真实最大C会员c，
任意六合法查询并会员o，令

B=Σc/(p+5)，M=Σo/[6(p+4c+1)]，N=Σo/[6(p+3c+2)]。

新普遍行是300u2+K−288B−12M−5N≥0。付款为同一真实source2强制C分支的
25源IC、三个中间CAP各1/2、末CAP1、同末BR平均1，再加5/12倍该分支内部
真第五源SAFE平均。把真实第五源收益留在同一客户成本中后取完整四尾最低值，
最后才用|C|=K；并未提前假设中间收益等于u2。两个六索引均值保真实d≥o。
当前仿射包络端点5/12由(p,c,o;r3r4r5r6)=(0,0,1;0010)支付；不声称所有钱包最优。
Main将新行代入整个1002最优面，精确恒为
−15981204499895866953854050884598865236619 / 86426960107246755980438461555855802597096
≈−.1849099456936224。

## 已冻结独审及已发现文字勘误

maximal_root_tail_wallet_v3_audit/及相邻.md已冻，独立检查270原行/129列/自由K,O的
131列和Main全局桥257列均PASS，manifest e670451f2d1b23c7d389ed4425074d9a2348969c9a76d0ed634903f443ef1cb8。
Main实读发现其相邻正文COST显示式首行三分式漏印两个加号；实际check_exact.py
及证书使用相加，计算不受影响。准确首行必须是

126000q/(b+1+r+y+t) + (43r+31218y+34458t)/(b+b3+3)
+ 1654(r+y+t)/(b+b3+b4+b5+1)，再加后两行5400与7740项。

这是明确文字勘误，不能按旧展示式中的乘积引用。独审者将在新的
visible_c_source2_equality_audit/root270_formula_erratum.md保正式勘误，旧冻结字节不改。
原根270数学证明与Main全131检查此前已正确，正式source3引理不引用这份错误展示。

## 正式登记及待集成的边

Stage16已新增唯一正式source3/root引理M-a90ca74cfdc848cb8f628fac8dd35f0a。
本次按版本规则升至v2，只将公式NU行末TeX空白写为quad；body SHA
25e68dd35cedd7bc507092111a96fb8dd1b26f2e507275597915c763c5376676。
计算对象cross-branch-necessary-system-20261111升v13，仅刷新引理证据SHA；
其Stage16承重正文不变，仍准确回流到CAP4普遍界.4400737002661185。
后续root270/.44026194及可见C/.44033437、新定量行属于完整已核工作包，下一版定向回流。
旧冻结draft body.md原字节及正式v1原字节保存在registration/stage16_whitespace_correction/
的确定性gzip内。仅原draft文本不入此次提交，其SHA256SUMS在恢复原稿后仍匹配。
没有改输入、覆盖失败回执或绕过Git空白检查。

登记实际3793对象，4986材料；canonical edge_files保持2114。
本次8条受影响边均已正规重新bind/check。此前10条自有边漏canonical索引加本轮3条，
仍须在隔离mapper完成实际plan/claim/published receipt/done/assemble；不手改edge_files。
mapper /workspace/scratch/b0fef5ec503f/co-work-anl-boss1-map，Boss1/map-v2，旧3任务不动。
Main先确认本轮pushed，再同步mapper固定当前注册pin并做这个窄比较。

## 当前实际代理及下一步

/root/visible_maximum_joint已闭合1002输入准备，其实际独立worker为
/root/visible_maximum_joint/independent_precheck，0优化。
/root/visible_maximum_joint_solve已闭合唯一1002求解/原对偶/整面排除；同一代理新义务
只准备visible_maximum_joint_v2/的1003raw/513/2：旧1002字面全保，仅追加Main新行。
此下一输入尚无优化授权，不能重跑旧求解；冻结审核后由Main另行释放唯一求解。
/root/early_shared_x_source_audit完成751与root270独审，现写新的
visible_c_source2_equality_audit/：独立整面中间真源SAFE矛盾及文字勘误；随后另审
main_source2_maximum_nested_safe/的真实预算与全部128态/513系数，0优化。

751点无关模板已冻但未绑定任何新点；旧225/546/867/1002完整面均已被廉价真约束排除，
不再消耗这些点的phase-I。唯一云请求C-six-boss1-common-x-joint-23676-01，
run43096304349，源b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad，最后check10 queued，
jobs/artifacts空；没有重发、取消或绕本地大型求解守卫。固定16hist值与普遍界严格区分。
Main持续推导、核查、保存和推进；checkpoint不结束开放原题。
'''


def main():
    out=HERE/'stage16b-save-receipts.json'
    assert not out.exists()
    assert json.loads((WS/'main_visible_c_certificate_check.json').read_text())['status'].startswith('PASS_MAIN')
    assert len(json.loads((HERE/'stage16b-edge-receipts.json').read_text()))==16
    # Preserve the failed stderr bytes without re-introducing their quoted trailing spaces.
    raw=HERE/'stage16_whitespace_correction/failed-checkpoint-stage16.stderr.txt'
    data=raw.read_bytes()
    zipped=Path(str(raw)+'.gz')
    zipped.write_bytes(gzip.compress(data,mtime=0))
    assert gzip.decompress(zipped.read_bytes())==data
    raw.unlink()
    (HERE/'stage16b-current.md').write_text(NOTE)
    (WS/'assignments/stage16b.md').write_text(NOTE)
    mp=WS/'main.md'
    old=mp.read_text()
    headline='# Boss1：六人共同目录跨真实分支研究\n\n'
    assert old.startswith(headline) and '## Stage16b当前入口' not in old
    mp.write_text(headline+'## Stage16b当前入口\n\n'+NOTE+'\n'+old[len(headline):].replace('## Stage16当前入口','## Stage16历史入口',1))
    readme=REPO/'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'
    readme.write_text('# Boss1：恰六人半覆盖\n\n实际研究clone：/workspace/scratch/b0fef5ec503f/co-work-anl-boss1。\n\n恢复先打开research/workspaces/six-boss1-20261111/main.md顶部Stage16b、spec.json及其实际证据路径，再research resume six-boss1-20261111。同Boss、分支、存档与子档start --resume。\n\n'+NOTE)
    tasks=[
        ('main','registration/stage16b-current.md','working','/root','确认Stage16b pushed；正规mapper窄范围集成；核新nestedSAFE独审和1003输入，继续原题。'),
        ('visible_maximum_joint','visible_maximum_joint.md','closed','/root/visible_maximum_joint','冻结输入已Main全列实核，唯一1002求解由另一实际agent闭合。'),
        ('visible_maximum_joint_solve','visible_maximum_joint_solve.md','closed','/root/visible_maximum_joint_solve','1002原对偶及全最优面排除已冻且Main全域重放；仅必要锥，无SPE反例。'),
        ('visible_maximum_joint_v2','assignments/stage16b.md','working','/root/visible_maximum_joint_solve','只准备1003raw新输入，原1002不动；未授权优化。'),
        ('maximal_root_tail_wallet_v3_audit','registration/stage16b-current.md','closed','/root/early_shared_x_source_audit','270/129/131及全局257桥独审闭合；Main发现COST漏两个加号，已在本笔记准确更正，另份勘误待回。'),
        ('visible_c_source2_equality_audit','assignments/stage16b.md','working','/root/early_shared_x_source_audit','独立整面内部源SAFE与弱平局；随后独审Main新普遍nestedSAFE，0优化。'),
    ]
    receipts=[]
    for solver,note,state,agent,nextstep in tasks:
        args=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full','--note',str((WS/note).relative_to(REPO)),
              '--state',state,'--agent-id',agent,'--next',nextstep]
        r=subprocess.run(args,cwd=REPO,capture_output=True,text=True)
        prefix=HERE/('stage16b-save-'+solver)
        Path(str(prefix)+'.stdout.json').write_text(r.stdout);Path(str(prefix)+'.stderr.txt').write_text(r.stderr)
        if r.returncode: raise RuntimeError((solver,r.stderr))
        receipts.append(dict(solver=solver,result=json.loads(r.stdout)))
        print('saved '+solver,flush=True)
    out.write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()

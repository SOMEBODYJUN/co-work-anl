"""Save the actual Stage15 mathematics and continuation obligations serially."""
from pathlib import Path
from hashlib import sha256
import subprocess
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=HERE.parents[3]
RUN='six-boss1-20261111'
PREFIX='research/workspaces/'+RUN+'/'


def main():
    receipt=HERE/'stage15-save-receipts.json'
    assert not receipt.exists()
    for name in ['main_thirty_index_strengthening','main_background_projection','main_all_source31_family']:
        folder=WS/name
        assert not (folder/'manifest.json').exists()
        entries=[{'path':p.name,'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
                 for p in sorted(folder.iterdir()) if p.is_file()]
        (folder/'manifest.json').write_text(json.dumps({'status':'FROZEN_MAIN_PROOF_AND_EXACT_OUTPUTS','optimizer_calls':0,
              'files':entries,'scope':'Only these original files; later audits and additional consequences have independent paths.'},ensure_ascii=False,indent=2)+'\n')
    entry='''## Stage15当前入口：30对真实预算、225行普遍界与全部源31组合

Boss1；RUN six-boss1-20261111；研究分支rebuild/research-v2；customer-attraction/six-providers。原六人2W≥OPT6仍OPEN，Main继续推导。写本入口时最后实际确认pushed为6af9f623faf22f2a1f0d668884f40e10a368404a；Stage15以随后实际pushed回执为准。

### 已完成且可独立接续的数学

v3_optimum_joint_face/已冻：完整221最优面是不可见z0射线×准确闭区间；actual C36重查询在整面恒负。全257列保号步给普遍界1826371831495384107652782239761/4226481233718360768948158386755≈.432125858485969。Main已独立重放该严格证书的全列。原v3代表点末位SAFE6(X)平局未被传播到整面。

maximal_root_tail_wallet_v2/和独立audit/已冻：原根71加C36一行，唯一129列LP，固定v3 K的匹配精确最优；独立自由K/O的131列恒等式给229185173551068u≥23463022015563K+4570807634338O，O可为任意六合法查询并。Main全72原始行、质量式、131列亲核PASS。

Main从既有强PAIR任意索引聚合正文识别30个有序异索引对的强覆盖并成本o/(3D)，无需菜单分割，重复标签仍可。以相同九权重算全部128型/2048态的C30，再保留根72十权并精确提高O自由乘子η=10132956584/286481466938835，给ROOT30：1145925867755340u≥117315110077815K+22894569998026O。新根线是固定权非负证明，未声称新根锥最优。main_thirty_index_strengthening/含完整证明、全部余项及四个全257新行；第二位独立审计也核131列PASS。

universal_union_wallet_v4/已冻：保221旧行，加入actual C30、actual RC30、源2(T=A6,Q=X)31行、ROOT30，共225raw/213unique/257cols，唯一LP41迭代。精确原始/对偶给alpha4=393354291273355731388235883588451948/899229760032273191421693253016184735≈.43743468994980583，K=157883277027938710045013551506238954/899229760032273191421693253016184735。11正预算、243正客户余项；全部256型保留。Main全225/257及四行逐系数复核PASS，见main_universal_wallet_v4_check.py/.json。输入b520abb…，证书290f90…，冻结manifest bde90c…；不是SPE反例。

该225点在源2、T=A5、Q=A6的合法31通式值为−104997578333106831070437069794935859/899229760032273191421693253016184735；T=A5,Q=X也严格负。Main进一步证明前五个真实源统一族：n=6−i，31u_i+nK≥n|T|+30Σ_T1/(p+n+1)+Σ_Q1/(p+1+n1_T)。456隐藏态/60闭式最小值，7个纯合法角色和六标签菜单均值组成5×8×8=320行，双均值用30异索引。Main与独立审计均逐82240列核完；15行切225代表点。main_all_source31_family/已保存全族；它是既有portfolio的显式参数族，不另认通用方法。

Main把已登记一背景五尾原53权证书的全6144×2表经六删一和d∈[o,6o]投影到全部256型。保V=W−u1、准确删槽损失及κ=226487/10^21的K列，不把利润当覆盖。该BG-PROJ排221点但225点余量+.0035725761253049483，因此没有宣称它排当前点。完整推导与257列在main_background_projection/；原大型oracle未重跑，仅继承已登记完整域证明并核原表的12288条件项。

actual_source2_opt_requery/及独立audit已冻结SYMBOLIC_UNBOUND：243真预算，未来s个正可见型对应32s物理列、s质量等式、243+2s原始不等式，完整切割域8192。当前无绑定点/无矩阵/0优化器。225点已被显式31族排除，故不在这个已排点上浪费phase-I；等下一546行点。

### 当前真实代理与下一步

/root/universal_union_wallet_lp：v4已闭合，现只写universal_union_wallet_v5/。Main已正式释放唯一546raw/257col LP（225旧+320source31+1BG），须先独立前检、正行缩放，保raw重复、K微小负列、完整原始/对偶和冻结输入。family SHA0268bef0a826fc1872f9b7ec7fa5d0433b1730b8670d69098a9d2c8edb5dedfd；BG最终SHAf39ae91167d96f015c188159e3efb9dcbf7436640e058467b0ead1386c4744cc。不得静默重跑。

/root/universal_true_x_tail：source2模板已冻，现v4_source2_identity/只做0优化器线代。初步已核225整面2维（X交换方向+z0）及SAFE2(A5)、两K帽恒紧；须保存全域signed身份和同一真实A5偏离四尾覆盖刚性。完成后沿原席接v5准确点的243源阶段I；尚无该阶段I授权。

/root/early_shared_x_source_audit：source2模板与ROOT30审计已冻；source31_family_audit/全456态/960菜单/3840混合/82240列已PASS，正在冻结文字。之后独立核下一v5真实源模板及点释放，不替构建方运行优化器。

### 形式回流、图索引与云端的准确状态

最后正式登记仍为Stage14两条父档引理v1及计算对象v11。上述Stage15新数学已经在实际工作区完整保存，下一步定向写正文与v12增量；源3重查询的新稳定ID已分配为M-a90ca74cfdc848cb8f628fac8dd35f0a，只用该ID，不重复申请。

发现此前十个本RUN边文件虽已push/edge-check，却不在registry.edge_files，不能说canonical图接回完成。另一个隔离mapper clone /workspace/scratch/b0fef5ec503f/co-work-anl-boss1-map 已按Boss1、map-v2、同结果分支start --resume成功并doctor write-verified；原研究clone/RUN/存档绑定未动。首次网络clone超时的仅.git残件已保留，后用无硬链接本地独立copy并正规start同步。旧mapper任务不抢领不改写；将按正式plan/claim/receipt/done/assemble路径补本轮定向边，不能手工追加绕过集成检查。尚未做map共享写入。

唯一Actions run43096304349、source b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad仍queued；check9 jobs/artifacts均空，无重发、无本地绕过。固定16hist路线W10≈.4941319648不是本全256型普遍界。

'''
    p=WS/'main.md'; text=p.read_text();assert '## Stage15当前入口：' not in text
    text=text.replace('## Stage14当前入口：','## Stage14历史入口：',1)
    first,rest=text.split('\n',1);p.write_text(first+'\n\n'+entry+rest.lstrip())
    (WS/'assignments/stage15.md').write_text('# Stage15实际派工与恢复\n\n'+entry)
    (REPO/'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md').write_text('''# Boss1：恰六人半覆盖

RUN：six-boss1-20261111；Boss1；分支rebuild/research-v2；存档customer-attraction；子档six-providers。

实际研究clone：/workspace/scratch/b0fef5ec503f/co-work-anl-boss1。恢复先读research/workspaces/six-boss1-20261111/main.md顶部Stage15及spec.json，再打开实际证明/程序/输入/输出并research resume six-boss1-20261111。原环境丢失时同Boss、分支、存档、子存档start --resume。

写本入口时最后确认pushed：6af9f623faf22f2a1f0d668884f40e10a368404a，checkpoints/stage14.json。Stage15须以实际pushed回执确认后才成为新恢复上限。原题仍OPEN，checkpoint后继续研究。

当前已核普遍下界为W≥393354291273355731388235883588451948/899229760032273191421693253016184735·OPT6≈.43743468994980583·OPT6。来自225原行/全部256客户型及K的精确非负对偶，Main全225/257重放PASS。该必要系统代表点被源2真改A5后的末位查询严格排除，不是完整SPE反例。

新全source31族：i1..5，n=6−i，任意合法T,Q均有31u_i+nK≥n|T|+30Σ_T1/(p+n+1)+Σ_Q1/(p+1+n1_T)。已给320全257行，独立审计PASS，15行切225代表点。30异索引PAIR/RC、C30重查询及ROOT30完整来源和全域证书在main_thirty_index_strengthening/。既有背景五尾53权的全型投影在main_background_projection/，225点通过它，保准确利润/删槽账。

当前代理：/root/universal_union_wallet_lp做唯一获释546行v5；/root/universal_true_x_tail做225整面真实source2身份（0优化器），之后接新点；/root/early_shared_x_source_audit冻结320族独立审计。243行actual-source2符号模板及审计已冻，尚无绑定点/矩阵/phase-I。原低点已被简单族排，不对它继续阶段I。

正式登记当前仍是Stage14计算v11和两父档v1；Stage15新数学准备回流。源3新ID M-a90ca74cfdc848cb8f628fac8dd35f0a已保存。十个本RUN边文件的canonical索引漏接已识别；隔离mapper clone已正规恢复并doctor通过，尚未改共享图。不要把已推边文件当成已集成超边。

原云任务C-six-boss1-common-x-joint-23676-01、run43096304349仍queued，check9无jobs/artifacts，无重发。它的固定16hist数值不能替代全型界。
''')
    tasks=[
      ('v3_optimum_joint_face','v3_optimum_joint_face.md','closed','/root/universal_union_wallet_lp','完整221面、严格全域界与31附录已冻；不改旧包。'),
      ('maximal_root_tail_wallet_v2','maximal_root_tail_wallet_v2.md','closed','/root/universal_true_x_tail','根72精确原对偶及自由K/O线已冻，Main亲核。'),
      ('maximal_root_tail_wallet_v2_audit','maximal_root_tail_wallet_v2_audit.md','closed','/root/early_shared_x_source_audit','根72全部来源、原行及131列独立通过。'),
      ('actual_source2_opt_requery','actual_source2_opt_requery.md','closed','/root/universal_true_x_tail','243行SYMBOLIC_UNBOUND已冻；未来点必须Main另行释放，未调用phase-I。'),
      ('actual_source2_opt_requery_audit','actual_source2_opt_requery_audit.md','closed','/root/early_shared_x_source_audit','243静态来源及ROOT30全131列独立通过并冻结。'),
      ('universal_union_wallet_v4','universal_union_wallet_v4/summary.md','closed','/root/universal_union_wallet_lp','225精确原对偶与后验点诊断已冻；所有旧包只读。'),
      ('source31_family_audit','assignments/stage15.md','working','/root/early_shared_x_source_audit','456态/60min/82240列已PASS，仅收尾冻结。'),
      ('v4_source2_identity','assignments/stage15.md','working','/root/universal_true_x_tail','0优化器完成225整面及真实A5分支身份，保存全列。'),
      ('universal_union_wallet_v5','assignments/stage15.md','working','/root/universal_union_wallet_lp','已正式释放唯一546raw/257col LP；先前检并保全输入，全域有理恢复后给下一true-source2义务。'),
      ('main','main.md','working','/root','Stage15确认pushed后，定向正文/登记/正式图集成；继续v5真实重查；原题OPEN。')]
    receipts=[]
    for solver,note,state,aid,nxt in tasks:
        args=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full','--note',PREFIX+note,
              '--state',state,'--agent-id',aid,'--next',nxt]
        result=subprocess.run(args,cwd=REPO,capture_output=True,text=True)
        (HERE/f'stage15-save-{solver}.stdout.json').write_text(result.stdout)
        (HERE/f'stage15-save-{solver}.stderr.txt').write_text(result.stderr)
        if result.returncode:raise RuntimeError((solver,result.stderr))
        receipts.append({'solver':solver,'state':state,'actual_agent_id':aid,'receipt':json.loads(result.stdout)})
        print(solver+':'+state,flush=True)
    receipt.write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()

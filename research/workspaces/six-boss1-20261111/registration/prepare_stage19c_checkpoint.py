"""Save closed actual mathematics and RUN state; no live writer directory staged."""
from pathlib import Path
from hashlib import sha256
import gzip
import json
import subprocess

HERE=Path(__file__).resolve().parent
W=HERE.parent
R=W.parents[2]
PREFIX=str(W.relative_to(R))+'/'
RUN='six-boss1-20261111'
assert not (HERE/'stage19c-save-receipts.json').exists()
assert json.loads((W/'main_visible_c_v6_preflight.json').read_text())['status']=='PASS_MAIN_FULL4177_LITERAL_SOURCE_CONCATENATION_AND_CORRECT_MODEL'
assert json.loads((HERE/'stage19-edge-checks.json').read_text())['status']=='PASS_ALL_ELEVEN_BOUND_EDGES'

target=W/'visible_maximum_joint_v6/row_catalog.tsv'
raw=target.read_bytes()
folder=W/'portable_frozen_text_stage19c'
folder.mkdir(exist_ok=False)
archive=folder/'visible_c_v6_row_catalog.tsv.gz'
archive.write_bytes(gzip.compress(raw,mtime=0))
assert gzip.decompress(archive.read_bytes())==raw
manifest={'scope':'Lossless frozen4177 TSV storage; preserve all empty trailing fields and original source SHA.',
 'files':[{'target':'visible_maximum_joint_v6/row_catalog.tsv','archive':'portable_frozen_text_stage19c/visible_c_v6_row_catalog.tsv.gz',
           'sha256':sha256(raw).hexdigest(),'archive_sha256':sha256(archive.read_bytes()).hexdigest(),
           'original_bytes':len(raw),'freeze_manifest_sha256':sha256((W/'visible_maximum_joint_v6/freeze_manifest.json').read_bytes()).hexdigest()}]}
(folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
note=(W/'stage19c-current.md').read_text()
(R/'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md').write_text('# Boss1：恰六人半覆盖\n\n'+note)
main=W/'main.md';old=main.read_text();headline='# Boss1：六人共同目录跨真实分支研究\n\n'
assert old.startswith(headline)
main.write_text(headline+note+'\n## 以前阶段的历史记录\n\n'+old[len(headline):])
(W/'assignments/stage19c.md').write_text(note)
tasks=[
 ('source2_conditional_redistribution','source2_conditional_redistribution.md','closed','/root/source2_conditional_redistribution','完整δ180已冻结，Main全域核查；进入4177固定输入，不改旧3056。'),
 ('source1_lambda_complete','source1_lambda_complete.md','closed','/root/source1_lambda_complete','[0,25]整域同构旧族，无新增900行；新的λ≥25交独立义务。'),
 ('delta_uniform_audit','delta_uniform_audit.md','closed','/root/delta_uniform_audit','γ36完整证书及十正来源已Main全核，普遍界约.44175918841743164。'),
 ('visible_joint_v6_prepare','visible_maximum_joint_v6.md','closed','/root/visible_joint_v6_prepare','4177已冻结并Main核；旁挂X最大潜力条件更正必须与冻合同合读，不改输入。'),
 ('visible_joint_v6_solve','visible_maximum_joint_v6_solve.md','working','/root/visible_joint_v6_solve','静态骨架已停写、0LP授权；等Main图集成安全同步后凭最终SHA专门释放。'),
 ('stage19_formal_extensions','assignments/stage19c.md','closed','/root/stage19_formal_extensions','两个完整解析草稿由Main通读修正并正式接回新引理/计算v14。'),
 ('source2_cap3_tradeoff','assignments/stage19c.md','working','/root/source2_cap3_tradeoff','全h真实条件最小、186端点可能族；C-only冗余须证明，一般T/ordered继续。'),
 ('high_lambda_closure','assignments/stage19c.md','working','/root/high_lambda_closure','λ≥25全域/全部rays，验证真实SAFE与客户余项的完整闭合。'),
 ('Main','main.md','working','/root','正式checkpoint并完成定向map替代/assemble；安全同步，单独释放4177一次LP，接回当前数学义务，原half继续。')]
receipts=[]
for solver,nn,state,agent,nxt in tasks:
 args=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full','--note',PREFIX+nn,'--state',state,'--agent-id',agent,'--next',nxt]
 p=subprocess.run(args,cwd=R,capture_output=True,text=True)
 (HERE/f'stage19c-save-{solver}.stdout.json').write_text(p.stdout)
 (HERE/f'stage19c-save-{solver}.stderr.txt').write_text(p.stderr)
 assert p.returncode==0,(solver,p.stderr)
 receipts.append({'solver':solver,'state':state,'agent':agent,'receipt':json.loads(p.stdout)})
 print(solver+':'+state,flush=True)
(HERE/'stage19c-save-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
print('Stage19c RUN and closed frozen text saved',flush=True)

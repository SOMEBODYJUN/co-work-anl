"""Read-only delivery and finite exact endpoint checks; never invokes original mains."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib,json,math,re

STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-security-closure-and-uniform-root-primary')
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
EV=Path('archives/customer-attraction/tools/evidence/security-closure-uniform-root-primary')
WS=Path('cleanup/workspaces/Boss4/r3-security-closure-and-uniform-root-primary')
EXPECTED={'ceaf1282ad9019816dd7','9e72daa5a0b2a448316c','5d844d4f9cc725a3d288','ed3eaf5a278ffefe256c','f4a36f001a7aed051f24'}
def read(p):return json.loads((STAGE/p).read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def compositions(n,p):
    if p==1:
        yield (n,);return
    for a in range(n+1):
        for t in compositions(n-a,p-1):yield (a,)+t

def main():
    sm=read(EV/'source-manifest.json');pm=read(EV/'primary-manifest.json');rm=read(EV/'runtime-manifest.json')
    receipt=read(WS/'semantic-receipts.json');claim=read(WS/'claim-receipt.json');obs=read(WS/'claim-observation.json')
    assert claim['status']=='pushed' and claim['actor']=='Boss4'
    assert EXPECTED <= set(claim['ids'])
    assert obs['capture_sha256']==sha((STAGE/WS/'claim-receipt.json').read_bytes())
    assert claim['remote_tip']==sm['claim_push']==obs['remote_tip']=='f8aec6ba937b8d78e8c31f77a54296dc03f2df0f'
    assert {r['id'] for r in pm['sources']}==EXPECTED=={r['id']for r in receipt}
    assert len(receipt)==len(pm['sources'])==5 and len(rm['sources'])==11 and len(sm['sources'])==16
    assert sum(r['size']for r in pm['sources'])==22303
    assert sum(r['size']for r in rm['sources'])==488699
    for row in sm['sources']:
        raw=(STAGE/row['saved_path']).read_bytes()
        assert len(raw)==row['size'] and sha(raw)==row['sha256']
        assert len(row['sources'])==2 and all(s['bytes_verified']for s in row['sources'])
    for row in receipt:
        assert row['disposition']=='integrated'
        assert all(row[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for t in row['targets']:
            assert (STAGE/t).is_file()
    policies=read(EV/'uniform-input-structure.json')
    assert policies['distinct_policy_count']==3 and len(policies['inputs'])==4
    actions=[]
    for r in policies['inputs']:
        ac={tuple(x['history']):x['action'] for x in r['complete_actions']}
        p=r['topics'];m=r['players']
        assert p==6 and len(ac)==sum(p**k for k in range(m))==r['ordered_decision_histories']
        histories={()}
        expected=set()
        for k in range(m):
            expected.update(histories)
            histories={h+(a,)for h in histories for a in range(p)}
        assert set(ac)==expected and all(0<=a<p for a in ac.values())
        path=()
        for k in range(m):path+=(ac[path],)
        assert list(path)==r['actual_path']
        actions.append(ac)
    assert actions[0]==actions[1] and actions[2]!=actions[3]
    ur=read(EV/'replay-uniform/multisets_report.json')
    assert [r['LPs']for r in ur]==[56,56,111,111] and sum(r['LPs']for r in ur)==334
    assert [r['best']['normalized_violation']for r in ur]==[-0.5579710144927535,-0.5579710144927535,-0.0,-0.0]
    assert [r['best']['comparison_counts']for r in ur]==[[0,1,0,0,1,1]]*2+[[1,3,0,0,0,0]]*2
    assert all('candidate'not in r and r['scope']=='finite floating observations only'for r in ur)
    endpoints={}
    exact_vectors=0
    nonendpoint_vectors={}
    for m in [3,4]:
        p=6;vertices=set()
        for k in range(1,min(m,p)+1):
            for s in combinations(range(p),k):
                for a in s if k<m else (s[0],):
                    vertices.add(tuple(int(b in s)+(m-k if b==a else 0)for b in range(p)))
        want=sum(math.comb(p,k)*(k if k<m else 1)for k in range(1,min(m,p)+1))
        assert len(vertices)==want=={3:56,4:111}[m]
        total=0;nonvertex=0
        for n in compositions(m,p):
            total+=1;s=tuple(a for a,v in enumerate(n)if v);k=len(s);M=m-k
            if n not in vertices:nonvertex+=1
            if M:
                lam={a:F(n[a]-1,M)for a in s}
                assert sum(lam.values())==1 and all(x>=0 for x in lam.values())
                for b in range(p):
                    value=sum(lam[a]*(int(b in s)+(M if b==a else 0))for a in s)
                    assert value==n[b]
            else:assert n in vertices
            exact_vectors+=1
        assert total==math.comb(p+m-1,m)
        endpoints[str(m)]=want;nonendpoint_vectors[str(m)]=nonvertex
    assert exact_vectors==182 and nonendpoint_vectors=={'3':0,'4':15}
    rr=read(EV/'replay-root-weak/cone_security_probe_root_12.5.json')
    assert len(rr['trace'])==32 and rr['best']==rr['trace'][0]
    assert {(r['start'],r['iteration'])for r in rr['trace']}=={(s,i)for s in range(16)for i in range(2)}
    for r in rr['trace']:
        assert r['W']==1.0 and r['v']==0.07692307692307693 and r['true_gap']==-0.038461538461538436
        assert r['p']==[1.,0.,0.,0.,0.,0.] and r['weights']==[[63,1.]]
        if r['iteration']==1:assert r['cone_margin']==-0.038461538461538436
    assert F(25,2)*F(1,13)-1==F(-1,26)
    byid={r['id']:r for r in sm['sources']}
    executions=[]
    for kind,rid in [('root-weak','9e72daa5a0b2a448316c'),('uniform','f4a36f001a7aed051f24')]:
        e=read(EV/f'replay-{kind}/execution.json')
        assert e['status']=='finished'and e['exit_code']==0 and e['original_main_executions']==1
        assert e['code_and_input_bytes_unchanged'] and e['generated_report_byte_identical_to_frozen']
        raw=(STAGE/EV/f'replay-{kind}'/Path(byid[rid]['path']).name).read_bytes()
        assert raw==(STAGE/byid[rid]['saved_path']).read_bytes() and sha(raw)==e['generated_report_sha256']
        assert (STAGE/EV/f'replay-{kind}/stderr.txt').read_bytes()==b''
        for sid in e['actual_dependency_ids']:
            row=byid[sid];assert sha((STAGE/EV/'replay-tree'/row['path']).read_bytes())==row['sha256']
        executions.append({'kind':kind,'original_main_executions':1,'exit_code':0,'wall_seconds':e['wall_seconds'],'report_sha256':sha(raw)})
    links=0
    for p in (STAGE/'archives/customer-attraction/state').rglob('*.md'):
        text=p.read_text()
        assert all(k+':'in text for k in ['id','kind','type_tag','title','status','summary','source_refs'])
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://'in target or target.startswith('#'):continue
            rel=Path(__import__('os').path.normpath(str(p.parent.relative_to(STAGE)/target.split('#')[0])))
            assert (STAGE/rel).exists()or(REPO/rel).exists(),(p.name,target)
            links+=1
    return dict(status='pass',primary_count=5,primary_bytes=22303,runtime_dependencies=11,runtime_bytes=488699,original_sources_hashed=16,complete_action_tables_checked=4,different_action_tables=3,uniform_LP_calls=334,root_weak_LP_calls=65,root_trace_rows=32,exact_endpoint_decompositions=exact_vectors,endpoint_task_counts=endpoints,omitted_interior_counts=nonendpoint_vectors,local_formal_links_resolved=links,original_executions=executions,limits='Structural/hash and 182 exact finite vector identities only; original mains are never called here. Universal endpoint and W-normalization proofs are in the lemma; no numeric upper-bound dual or HALF theorem is certified.')

if __name__=='__main__':
    result=main();(STAGE/WS/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))

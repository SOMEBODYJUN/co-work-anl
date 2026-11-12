"""Pure JSON lossless display codec. Does not evaluate a game or replay an audit."""
import json, hashlib
from pathlib import Path
BASE = Path('/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1')
OUT = Path(__file__).parent
POLICY = 'archives/customer-attraction/tools/evidence/terminal-price-boss4/original/four_price_best.json'
REPORT = 'archives/customer-attraction/tools/evidence/saved-terminal-price-policies-definition-audit/report.json'
def hist(s): return [] if s == '_' else list(map(int,s))
def hs(v): return ''.join(map(str,v)) if v else '_'
def decode_policy(c):
    x = dict(c['fields_before_actions'])
    x['actions'] = [[hist(h),a] for h,a in c['actions']]
    x['instance'] = c['instance']
    x['certificate'] = dict(c['certificate_before_actions'])
    ix = range(len(x['actions'])) if c['certificate_order']=='same' else c['certificate_order']
    x['certificate']['actions']=[{'history':x['actions'][i][0], 'action':x['actions'][i][1]} for i in ix]
    return x

def decode_report(c):
    records=[]
    for rec in c['records']:
        x=dict(rec['metadata']); rows=[]
        for h,ch,ct,ds in rec['groups']:
            prefix=hist(h)
            chosen=prefix+hist(ct)
            for a,(s,slack) in enumerate(ds):
                rows.append({'history':prefix,'chosen':ch,'deviation':a,'chosen_terminal':chosen,'deviation_terminal':prefix+[a]+hist(s),'slack':slack})
        x['comparison_table']=rows;records.append(x)
    return records

def encode():
    raw=(BASE/POLICY).read_bytes();x=json.loads(raw)
    rows=[[hs(h),a] for h,a in x['actions']]
    byh={tuple(h):i for i,(h,a) in enumerate(x['actions'])}
    order=[byh[tuple(v['history'])] for v in x['certificate']['actions']]
    c={'format':'policy-dfs-pairs-v1','source':POLICY,'source_sha256':hashlib.sha256(raw).hexdigest(),'fields_before_actions':{k:v for k,v in x.items() if k in ['it','round','score','actual','root_action','z','clones']},'actions':rows,'instance':x['instance'],'certificate_before_actions':{'terminal_counts':x['certificate']['terminal_counts']},'certificate_order':'same' if order==list(range(len(rows))) else order,'trailing_newline':False}
    dec=json.dumps(decode_policy(c),ensure_ascii=False,indent=2).encode()
    assert dec==raw
    (OUT/'policy-codec.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    text=['POLICY FULL LOSSLESS READVIEW','All top-level nonaction fields:',json.dumps(c['fields_before_actions'],ensure_ascii=False,separators=(',',':')),'instance='+json.dumps(c['instance'],ensure_ascii=False,separators=(',',':')),'certificate_before_actions='+json.dumps(c['certificate_before_actions'],ensure_ascii=False,separators=(',',':')),'history _ is empty; digits are the original ordered label list; one pair per original top-level action, DFS order. certificate.actions is the SAME ordered list as dictionaries {history:list,action:int}.','Original actions, in source order:']
    text.extend(f'{h}:{a}' for h,a in rows)
    (OUT/'policy-readview.txt').write_text('\n'.join(text)+'\n')
    raw=(BASE/REPORT).read_bytes();xs=json.loads(raw);records=[]
    for x in xs:
        groups=[]; rows=x['comparison_table']
        for start in range(0,len(rows),6):
            rr=rows[start:start+6]; h=rr[0]['history']; ct=rr[0]['chosen_terminal']; ch=rr[0]['chosen']
            assert len(rr)==6 and ct[:len(h)]==h
            ds=[]
            for a,r in enumerate(rr):
                assert r['history']==h and r['chosen']==ch and r['chosen_terminal']==ct and r['deviation']==a and r['deviation_terminal'][:len(h)+1]==h+[a]
                assert list(r)==['history','chosen','deviation','chosen_terminal','deviation_terminal','slack']
                ds.append([hs(r['deviation_terminal'][len(h)+1:]),r['slack']])
            groups.append([hs(h),ch,hs(ct[len(h):]),ds])
        records.append({'metadata':{k:v for k,v in x.items() if k!='comparison_table'},'groups':groups})
    c={'format':'six-action-grouped-prefix-codec-v1','source':REPORT,'source_sha256':hashlib.sha256(raw).hexdigest(),'records':records,'trailing_newline':True}
    dec=json.dumps(decode_report(c),ensure_ascii=False,indent=2).encode()+b'\n'
    assert dec==raw
    (OUT/'report-codec.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    text=['REPORT FULL LOSSLESS READVIEW','Each row: h | chosen | chosen-terminal-suffix | deviation-suffix:slack for a=0,1,2,3,4,5 in that exact order.','_ denotes the empty ordered list. Each digit is one original numeric label. To decode: chosen_terminal=h+chosen-terminal-suffix; deviation_terminal=h+[a]+deviation-suffix.','Each group reconstructs six dictionaries with keys history,chosen,deviation,chosen_terminal,deviation_terminal,slack. No payoff or continuation was recomputed.']
    for i,rec in enumerate(records):
        text+=['RECORD '+str(i),json.dumps(rec['metadata'],ensure_ascii=False,separators=(',',':'))]
        for h,ch,ct,ds in rec['groups']:
            text.append(f'{h}|{ch}|{ct}|'+','.join(s+':'+slack for s,slack in ds))
    (OUT/'report-readview.txt').write_text('\n'.join(text)+'\n')
    verification={'method':'json decode, dictionary/prefix factorization only; reconstructed original indent-2 JSON bytes including sign of floating zero and trailing newline','policy':{'source_sha256':hashlib.sha256((BASE/POLICY).read_bytes()).hexdigest(),'decoder_sha256':hashlib.sha256(json.dumps(decode_policy(json.loads((OUT/'policy-codec.json').read_text())),ensure_ascii=False,indent=2).encode()).hexdigest(),'byte_equal':True},'report':{'source_sha256':hashlib.sha256(raw).hexdigest(),'decoder_sha256':hashlib.sha256(dec).hexdigest(),'byte_equal':True}}
    (OUT/'codec-verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(verification,ensure_ascii=False))
if __name__=='__main__':encode()

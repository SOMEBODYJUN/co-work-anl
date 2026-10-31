from pathlib import Path
import hashlib,json,subprocess,sys
E=Path(__file__).parent
ALIASES={'acc7b24f48eb613b5e07':'materialize_indexed.py','1264392684f36f1188f9':'strong_scan.py','3340d1960428251f0cbf':'strong_all_scan.py','f225ca9d4fb11f3dd1c9':'weak_scan.py','cc0969317188c8d2035a':'materialized_seed37381021_scale1000000.json','34a631cf8a586f330361':'weak_scan_best.json','7af45e3cd6dbd5503d48':'strong_scan_best.json','ae882b075f98b7f35b58':'strong_all_scan_best.json'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/'source-manifest.json').read_text()); assert len(m['sources'])==8
 for s in m['sources']:
  p=E/'source'/ALIASES[s['id']]; assert p.exists(),p; assert sha(p)==s['sha256'],(s['id'],sha(p),s['sha256'])
 src=json.loads((E/'source/materialized_seed37381021_scale1000000.json').read_text()); rep=json.loads((E/'replay/materialized_seed37381021_scale1000000.json').read_text())
 for k in src:
  if k!='seconds': assert src[k]==rep[k],k
 assert src['actual_ABCDE_is_SPE_outcome'] is False and src['root_outcomes']==1 and src['welfare']==1810296 and src['optimum']==2061696 and src['root_worst_counts']==[0,0,0,0,0,1,0,0,0,0,2,0,1,0,1]
 c=json.loads((E/'replay/candidates_verify.stdout').read_text()); assert c['passed'] and len(c['candidates'])==3
 expected={'34a631cf8a586f330361.json':('5','9','-1/5',781),'7af45e3cd6dbd5503d48.json':('4','7','0',156),'ae882b075f98b7f35b58.json':('4','7','0',156)}
 for x in c['candidates']: assert (x['welfare'],x['optimum'],x['objective'],x['verified_histories'])==expected[x['file']]
 for p in [E/'source/materialize_indexed.py',E/'source/strong_scan.py',E/'source/strong_all_scan.py',E/'source/weak_scan.py',E/'replay/verify_candidates.py']:
  subprocess.run([sys.executable,'-m','py_compile',str(p)],check=True)
 print(json.dumps({'passed':True,'source_count':8,'materialized_root_outcomes':1,'materialized_ABCDE_is_SPE_outcome':False,'candidate_certificates':3,'candidate_histories':[781,156,156]},ensure_ascii=False))
if __name__=='__main__': main()

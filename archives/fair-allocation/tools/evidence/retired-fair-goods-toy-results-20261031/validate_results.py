#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
p=ROOT/'toy_results.json'; b=p.read_bytes(); assert hashlib.sha256(b).hexdigest()=='13294bd3aafa5814a4f0570ef6c23da512e29ce53e88a1a055dafa41bcb5300c' and len(b)==5355
d=json.loads(b); assert d['boundary']=='all arithmetic integral; sampled valuation/ranking profiles only'
assert [(x['sizes'],x['rank'],x['feasible_labelled_allocations'],x['trials'],x['counterexample'],x['minimum_witness_count']) for x in d['keys']]==[
 ([3,3,2],2,864,5000,None,6),([3,3,3,3],3,31104,500,None,256)]
assert d['keys'][0]['lemma12_top_separation_allocations']==0 and d['keys'][1]['lemma12_top_separation_allocations'] is None
assert [(x['n'],x['copies'],x['allocation_count'],x['trials'],x['counterexample'],x['minimum_witness_count']) for x in d['copies']]==[
 (3,[1,1,2,2,2,1],729,5000,None,26),(4,[1,2,3,1,2,3],9216,2000,None,106)]
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hash_and_size':True,'key_fields':True,'copies_fields':True,'boundary':True},'interpretation':'Finite sampled valuation/ranking profiles only; no universal EF1/SD-EF1 theorem.'},ensure_ascii=False,indent=2)+'\n')
print('pass')

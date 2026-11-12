"""Lossless reading representation only; no mathematical audit or scientific entry.
Full original 1905 columns are represented, including all zero weights.
Blocks preserve actual column order. Each group has states [0,1],[1,0],[1,1].
Overlap pairs are all ordered itertools.combinations(group_ids,2).
Weight streams use [repeat_count, weight_dictionary_index], never discard zeros.
"""
import json, pathlib, itertools, hashlib, sys

def rle(xs):
 out=[]
 for k,g in itertools.groupby(xs):out.append([len(list(g)),k])
 return out

def unrle(xs):return [x for n,x in xs for _ in range(n)]

def encode(d):
 meta={k:v for k,v in d.items() if k!='certificate'}
 cm={k:v for k,v in d['certificate'].items() if k!='columns'}
 cols=d['certificate']['columns'];weights=[];groups=[]
 def wid(v):
  if v not in weights:weights.append(v)
  return weights.index(v)
 def gid(v):
  if v not in groups:groups.append(v)
  return groups.index(v)
 K=wid(cols[0]['weight']);assert cols[0]=={'kind':'K','weight':weights[K]}
 blocks=[];i=1
 while i<len(cols) and cols[i]['kind']=='hist':
  h=cols[i];n=i;i+=1;J=[]
  while i<len(cols) and cols[i]['kind']=='joint-reply':J.append(cols[i]);i+=1
  assert len(J)%3==0
  old=J[0]['hist_column_old'];gids=[];jweights=[]
  for a in range(0,len(J),3):
   tri=J[a:a+3];g=tri[0]['group'];gids.append(gid(g))
   for c,s in zip(tri,[[0,1],[1,0],[1,1]]):
    assert c['hist_column_old']==old and c['group']==g and c['state']==s
    assert set(c)=={'kind','hist_column_old','group','state','weight'}
    jweights.append(wid(c['weight']))
  assert set(h)=={'kind','actual_bits','d','hist','weight'}
  blocks.append([n,old,h['actual_bits'],h['d'],h['hist'],wid(h['weight']),gids,rle(jweights)])
 overlap=[]
 while i<len(cols):
  n=cols[i]['hist_column'];v=[]
  while i<len(cols) and cols[i]['kind']=='overlap' and cols[i]['hist_column']==n:v.append(cols[i]);i+=1
  b=next(b for b in blocks if b[0]==n);expected=[[groups[a],groups[b]] for a,b in itertools.combinations(b[6],2)]
  assert [x['groups'] for x in v]==expected
  assert all(set(x)=={'kind','hist_column','groups','weight'} for x in v)
  overlap.append([n,rle([wid(x['weight']) for x in v])])
 return {'format':'root-point-dictionary-sequence-v1','metadata':meta,'certificate_metadata':cm,'weight_dictionary':weights,'group_dictionary':groups,'K_weight':K,'hist_joint_blocks':blocks,'overlap_blocks':overlap}

def decode(e):
 weights=e['weight_dictionary'];groups=e['group_dictionary'];cols=[{'kind':'K','weight':weights[e['K_weight']]}]
 for n,old,bits,d,h,w,gids,stream in e['hist_joint_blocks']:
  assert len(cols)==n
  cols.append({'kind':'hist','actual_bits':bits,'d':d,'hist':h,'weight':weights[w]})
  vals=iter(unrle(stream))
  for g in gids:
   for s in [[0,1],[1,0],[1,1]]:cols.append({'kind':'joint-reply','hist_column_old':old,'group':groups[g],'state':s,'weight':weights[next(vals)]})
  assert next(vals,None) is None
 for n,stream in e['overlap_blocks']:
  b=next(b for b in e['hist_joint_blocks'] if b[0]==n);vals=iter(unrle(stream))
  for a,c in itertools.combinations(b[6],2):cols.append({'kind':'overlap','hist_column':n,'groups':[groups[a],groups[c]],'weight':weights[next(vals)]})
  assert next(vals,None) is None
 return {**e['metadata'],'certificate':{**e['certificate_metadata'],'columns':cols}}

if __name__=='__main__':
 p=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);raw=p.read_bytes();d=json.loads(raw);e=encode(d);assert decode(e)==d
 out.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
 result={'source_sha256':hashlib.sha256(raw).hexdigest(),'decoded_equals_original_json':True,'source_bytes':len(raw),'source_columns':len(d['certificate']['columns']),'encoded_bytes':out.stat().st_size,'weight_entries':len(e['weight_dictionary']),'group_entries':len(e['group_dictionary']),'lossless_scope':'all keys, scalars, floats, complete ordered columns, zeros and rational values; JSON structural equality; no audit executed'}
 out.with_name('point-readable-roundtrip.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

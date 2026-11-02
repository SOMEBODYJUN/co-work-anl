"""Exact literal checks of only the40 saved root assignments and their glue.
No NumPy, imported discover/build, original root verifier, all-cube pricing or LP.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
import argparse,json,hashlib,time,platform
HERE=Path(__file__).resolve().parent
P=HERE/'original/research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure'

def share(n,d):return F(n,d) if n else F()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args();start=time.perf_counter()
 source=P/'joint_atoms_exact.json';rf=P/'root_extension_exact.json';data=json.loads(source.read_text());root=json.loads(rf.read_text());K=F(data['K'])
 assert root['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest() and root['source_W']==data['W']
 paths=[[0,1,2,3,4,5],[0,5,6,7,8,9],[0,1,5,10,11,12]];assert root['root_paths']==paths
 names=[f'CAP:{j}' for j in range(1,13)]+['COPY:1','COPY:2']
 for k,path in enumerate(paths):
  for i in range(1 if k==0 else k+1,6):
   names += [f'FLOOR:{k}:{i}:{j}' for j in range(13) if j!=path[i]]
  names += [f'PAIR:{k}',f'LAST:{k}']
 assert len(names)==164
 specs=[['root_graph',n] for n in names]+[['actual_root_IC'],['maximum_equality',1],['maximum_equality',-1]]
 specs += [['actual_safe',i,j] for i in range(6) for j in range(13)]
 specs += [['actual_pair',i,j] for i in range(13) for j in range(i,13)]
 assert root['root_specs']==specs and len(specs)==336
 def coeff(a,d,b,spec):
  memberships=[[b[j] for j in path] for path in paths]
  profits=[[share(x,sum(v)) for x in v] for v in memberships]
  if spec[0]=='root_graph':
   fields=spec[1].split(':');kind=fields[0]
   if kind=='CAP':return b[0]-b[int(fields[1])]
   if kind=='COPY':
    k=int(fields[1]);return profits[0][k]-profits[k][k]
   if kind=='FLOOR':
    k,i,j=map(int,fields[1:]);return profits[k][i]-F(b[j],sum(memberships[k][:i])+6-i)
   k=int(fields[1]);v=memberships[k]
   if kind=='PAIR':
    p=sum(v[:4]);H=share(v[4]+v[5],sum(v))+F(v[4],(p+1)*(p+2));return 3*H+F(p,p+1)-int(d>0)
   assert kind=='LAST';p=sum(v[:5]);return 6*profits[k][5]+F(p,p+1)-int(d>0)
  if spec[0]=='actual_root_IC':return share(a[0],sum(a))-profits[0][0]
  if spec[0]=='maximum_equality':return -spec[1]*b[0]
  if spec[0]=='actual_safe':
   _,i,j=spec;return share(a[i],sum(a))-F(b[j],sum(a[:i])+6-i)
  assert spec[0]=='actual_pair';_,i,j=spec;p=sum(a[:4]);H=share(a[4]+a[5],sum(a))+F(a[4],(p+1)*(p+2));return H-F(b[i]+b[j],p+1)+F(b[i]*b[j],(p+1)*(p+2))
 masses=defaultdict(F);joint_indices=defaultdict(list)
 for j,atom in enumerate(data['atoms']):
  hist=data['histograms'][atom['hist_index']];key=hist['actual_bits'],hist['d'];masses[key]+=F(atom['weight']);joint_indices[key].append(j)
 recovered=defaultdict(F);root_indices=defaultdict(list);slacks=[F()]*336;scaled_rows=[]
 for i,spec in enumerate(specs):
  if spec[0]=='maximum_equality':slacks[i]=spec[1]*K
 for j,atom in enumerate(root['root_atoms']):
  a=tuple(map(int,atom['actual_bits']));d=atom['d'];key=atom['actual_bits'],d;mass=F(atom['weight']);b=atom['root_bits'];assert mass>0 and len(b)==13 and all(x in (0,1) for x in b)
  assert atom['root_assignment_index']==sum(bit*(1<<i) for i,bit in enumerate(b))
  recovered[key]+=mass;root_indices[key].append(j);row=[]
  for i,spec in enumerate(specs):
   c=coeff(a,d,b,spec);assert (60*c).denominator==1;row.append(int(60*c));slacks[i]+=mass*c
  scaled_rows.append(row)
 assert dict(recovered)==dict(masses) and len(masses)==8 and len(root['root_atoms'])==40
 assert min(slacks)==0 and all(v>=0 for v in slacks)
 assert root['verification']['minimum_integer_scaled_slack']==str(60*min(slacks))
 glue=[];jback=defaultdict(F);rback=defaultdict(F)
 for key,n in masses.items():
  for ji in joint_indices[key]:
   for ri in root_indices[key]:
    mass=F(data['atoms'][ji]['weight'])*F(root['root_atoms'][ri]['weight'])/n
    assert mass>0;glue.append({'joint_atom_index':ji,'root_atom_index':ri,'weight':str(mass)});jback[ji]+=mass;rback[ri]+=mass
 assert all(jback[j]==F(atom['weight']) for j,atom in enumerate(data['atoms']))
 assert all(rback[j]==F(atom['weight']) for j,atom in enumerate(root['root_atoms']))
 table=[{'actual_bits':key[0],'d':key[1],'mass':str(n),'joint_atoms':len(joint_indices[key]),'root_atoms':len(root_indices[key]),'conditional_product_atoms':len(joint_indices[key])*len(root_indices[key])} for key,n in sorted(masses.items())]
 report={'scope':'literal336 specified-row checks on only40 saved root assignments; exact conditional-product glue; not full SPE','input_joint_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'input_root_sha256':hashlib.sha256(rf.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'assertions_enabled':__debug__,'root_rows':336,'root_atoms':40,'saved_coefficients_checked':40*336,'scaled60_coefficients_by_root_atom':scaled_rows,'all_unscaled_slacks':[str(v) for v in slacks],'root_specs':specs,'zero_slacks':sum(v==0 for v in slacks),'positive_slacks':sum(v>0 for v in slacks),'actual_type_table':table,'conditional_product_atoms':len(glue),'glued_atoms':glue,'all_joint_and_root_marginals_recovered':True,'shared_K':str(K),'W':data['W'],'O':data['O'],'elapsed_seconds':time.perf_counter()-start,'original_entry_calls':0,'original_root_verify_calls':0,'all_cube_matrices_built':0,'LP_calls':0}
 args.output_dir.mkdir(parents=True,exist_ok=False);(args.output_dir/'all336-and-glue.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('scaled60_coefficients_by_root_atom','all_unscaled_slacks','root_specs','glued_atoms')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()

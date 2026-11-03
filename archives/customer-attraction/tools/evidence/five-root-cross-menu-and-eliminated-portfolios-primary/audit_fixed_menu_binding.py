"""One AST-isolated original newrow61-call binding; independent610 local states.
No original module import, Universe, LP, search or old4007-row re-verification.
"""
from pathlib import Path
from fractions import Fraction as F
import ast,argparse,json,gzip,hashlib,time,sys
E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();stage=next((p for p in E.parents if p.name=='deliverables'),None) or repo
 def resolve(z):
  q=stage/z['preserved_repo_path']
  if not q.exists():q=repo/z['preserved_repo_path']
  compressed=q.read_bytes();raw=gzip.decompress(compressed) if z['compression']=='gzip-lossless' else compressed
  assert len(raw)==z['size'] and sha(raw)==z['sha256'];return raw
 t=time.perf_counter();started=time.time();M=json.loads((E/'source-manifest.json').read_text());by={z['id']:z for z in M};related=json.loads((E/'related-manifest.json').read_text());raw=resolve(by['e3801b4fc38d6b71cc53']);source=raw.decode();tree=ast.parse(source)
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='newrow');out=E/'fixed-menu-binding';out.mkdir(exist_ok=True)
 (out/'original-newrow-source.txt').write_text(ast.get_source_segment(source,node)+'\n');(out/'original-newrow-AST.txt').write_text(ast.dump(node,include_attributes=True,indent=2)+'\n')
 globs={'F':F};exec(compile(ast.Module(body=[node],type_ignores=[]),by['e3801b4fc38d6b71cc53']['path'],'exec'),globs);original=globs['newrow']
 point_raw=resolve(next(z for z in related if z['id']=='5db6a037342bdee0f107'));point=json.loads(point_raw);atoms=point['atoms'];assert len(atoms)==61 and all(F(z['exact_mass'])>0 for z in atoms)
 expected1=json.loads(resolve(by['5c203feeb991f0926efe']));expected2=json.loads(resolve(by['3852a437d1d287e73e2b']))['results'][0]['exact_separator'];assert expected1['source_sha256']==sha(point_raw)
 atom_records=[];expanded=[];sumrow=F();summax=F();W=F();O=F();calls=0
 for i,z in enumerate(atoms):
  mass=F(z['exact_mass']);mb=list(map(int,z['max_bits']));p=sum(mb[:3]);tot=sum(mb);D,B=mb[3:];d=sum(z['AB_hist'][4:]);vD=F(D,tot) if D else F();vB=F(B,tot) if B else F();den=(p+1)*(p+2)
  value=original(z);calls+=1;choices=[]
  for ell in range(6):
   for h in range(max(0,d+ell-5),min(d,ell)+1):
    S=5*vD-F(d,p+1)+F(h,den);Z=5*vB-F(ell,p+D+1);V=F(d*ell-5*h,den)
    combo=(10*S+Z+2*V)/13
    cancelled=(10*(5*vD-F(d,p+1))+5*vB+ell*(F(2*d,den)-F(1,p+D+1)))/13
    assert combo==cancelled
    choices.append((ell,h,combo));expanded.append([i,ell,h,str(S),str(Z),str(V),str(combo)])
  best=max(v for ell,h,v in choices);assert F(13,10)*best==value
  sumrow+=mass*value;summax+=mass*best
  W+=mass*int(any(map(int,z['bits'][:5])));O+=mass*int(d>0)
  atom_records.append({'index':i,'max_bits':z['max_bits'],'d':d,'exact_mass':z['exact_mass'],'original_E_half':str(value),'maximum_normalized_combination':str(best),'maximizing_ell_h':[[ell,h] for ell,h,v in choices if v==best],'mass_times_E_half':str(mass*value),'mass_times_maximum':str(mass*best),'legal_states':len(choices)})
 assert calls==61 and len(expanded)==610
 assert W==1 and O==F(point['comparison_cover'])
 assert sumrow==F(expected1['row_sum'])<0 and summax==F(expected2['weighted_maximum'])<0 and F(13,10)*summax==sumrow
 assert expected2['lambda']=={'penult_true':'10/13','last_actual_menu':'1/13','reply_cross':'2/13'}
 dump(out/'atom-values.json',atom_records);dump(out/'all610-independent-states.json',expanded)
 result={'scope':'original AST function extracted61calls plus independent610state cancellation/maxima at fixed61atom input; no old4007-row qualification','input_sha256':sha(point_raw),'original_full_program_sha256':sha(raw),'original_function_source_sha256':sha((out/'original-newrow-source.txt').read_bytes()),'original_AST_sha256':sha((out/'original-newrow-AST.txt').read_bytes()),'required_real_globals':{'F':'fractions.Fraction'},'original_newrow_calls':calls,'independent_S_Z_V_state_expansions':len(expanded),'fixed_point_applications':{'E_half':1,'normalized_combination':1},'W_checked':str(W),'comparison_cover_checked':str(O),'E_half_total':str(sumrow),'normalized_combination_total':str(summax),'relation_13_over10':True,'both_saved_exact_values_equal':True,'zero_operations':{'original_main':0,'original_module_import':0,'Universe':0,'LP':0,'search':0,'old4007_row_build_or_recheck':0,'original_extend_rows':0,'original_oracle_audit':0,'four_SPE_construction_audit':0}}
 dump(out/'result.json',result)
 event={'attempt':1,'started_unix':started,'elapsed_seconds':time.perf_counter()-t,'python':sys.version,'exit_code':0,'assertions_enabled':__debug__,'script_sha256':sha(Path(__file__).read_bytes()),'original_full_source_sha256':sha(raw),'fixed_related_point_sha256':sha(point_raw),'preserved_point_after_sha256':sha(resolve(next(z for z in related if z['id']=='5db6a037342bdee0f107'))),'original_function_calls':61,'independent_state_expansions':610,'mathematical_run_attempts':1,'no_original_entrypoint_executed':True}
 dump(out/'execution.json',event);print(json.dumps({'E_half_total':str(sumrow),'normalized_combination_total':str(summax),'original_newrow_calls':61,'independent_state_expansions':610,'elapsed_seconds':event['elapsed_seconds']},indent=2))
if __name__=='__main__':main()

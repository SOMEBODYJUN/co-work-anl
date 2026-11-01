"""Independent reconstruction of the saved split Z masses and one joint atom lift.

No author module, matrix builder, optimizer or previously completed ZZ-row scan
is executed. Existing exact 60-row evidence is bound by hashes and reused.
"""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def group(g):
    return g[0],g[1],tuple(g[2]),tuple(g[3])


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def main():
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    e=a.repo/'archives/customer-attraction/tools/evidence'
    oldpath=e/'split-basic-graph-program/related/split_basic_exact.json'
    pointpath=e/'zz-threshold-closure-program/related/zz_split_exact.json'
    auditpath=e/'zz-threshold-closure-program/interface-audit.json'
    pairpath=e/'r5662-replay-reports-and-identity-boss3/related/pair_closure_exact.json'
    old=json.loads(oldpath.read_text());point=json.loads(pointpath.read_text());prior=json.loads(auditpath.read_text())['modes']['split'];pair=json.loads(pairpath.read_text())
    assert digest(pointpath)==prior['saved_sha256']=='312732da47c24fe39259c339cf669231162f1402c85a4036a8a351abaef7f51c'
    assert digest(oldpath)==point['source_sha256']==prior['source_sha256']=='b12c4aa6b3cd106f3fb8e8a56be7469988456c0cb6e02b1741db8c09d587b34a'
    assert len(point)==10 and len(old)==12
    assert point['rows']==4005 and point['variables_count']==275
    cols=old['columns'];assert len(cols)==1905
    weights=[F(c['weight']) for c in cols];assert min(weights)>=0
    hs={};hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':
            hi=j;hs[j]={'column':c,'groups':{}}
            assert c['d']==1 and sum(c['hist'])==6
        elif c['kind']=='joint-reply':
            g=group(c['group']);st=tuple(c['state']);assert st in {(0,1),(1,0),(1,1)}
            hs[hi]['groups'].setdefault(g,{})[st]=j
    assert len(hs)==16 and sum(len(h['groups']) for h in hs.values())==194
    expected=[];slabs=[];atoms=[];summary=[];new=[F()]*1905;new[0]=weights[0];all_marginals=[]
    for hi,h in hs.items():
        H=weights[hi];new[hi]=H;gs=h['groups'];rm={};before={};atomids=[]
        for g,states in gs.items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            assert sum(weights[j] for j in states.values())<=H
            rm[g]=weights[states[1,0]]+weights[states[1,1]]
            before[g]=weights[states[0,1]]+weights[states[1,1]]
        start=len(expected);slab_start=len(slabs)
        if H:
            cuts=sorted({F(),H,*rm.values()})
            for left,right in zip(cuts,cuts[1:]):
                mass=right-left;ids=[];ys=[];rs=[];groups=list(gs)
                assert mass>0
                for g in groups:
                    desc={'hist_column':hi,'left':str(left),'right':str(right),'group':[g[0],g[1],list(g[2]),list(g[3])],'r':int(right<=rm[g])}
                    v=point['variables'][len(expected)];assert {k:x for k,x in v.items() if k!='weight'}==desc
                    y=F(v['weight']);assert 0<=y<=mass
                    ids.append(len(expected));ys.append(y);rs.append(desc['r']);expected.append(desc)
                    states=gs[g]
                    if desc['r']:new[states[1,0]]+=mass-y;new[states[1,1]]+=y
                    else:new[states[0,1]]+=y
                sid=len(slabs);slab={'id':sid,'hist_column':hi,'left':str(left),'right':str(right),'mass':str(mass),'variable_indices':ids,'groups':[d['group'] for d in expected[-len(ids):]],'R_bits':rs,'Z_masses':list(map(str,ys)),'atom_indices':[]}
                zcuts=sorted({F(),mass,*ys})
                for low,high in zip(zcuts,zcuts[1:]):
                    zb=[int(high<=y) for y in ys];idx=len(atoms);atomids.append(idx);slab['atom_indices'].append(idx)
                    atoms.append({'id':idx,'slab':sid,'hist_column':hi,'left_in_slab':str(low),'right_in_slab':str(high),'mass':str(high-low),'R_bits':rs,'Z_bits':zb})
                assert sum(F(atoms[i]['mass']) for i in slab['atom_indices'])==mass
                for j,y in enumerate(ys):assert sum(F(atoms[i]['mass'])*atoms[i]['Z_bits'][j] for i in slab['atom_indices'])==y
                slabs.append(slab)
        for g,st in gs.items():
            rnew=new[st[1,0]]+new[st[1,1]];znew=new[st[0,1]]+new[st[1,1]]
            assert rnew==rm[g]
            assert H-sum(new[j] for j in st.values())>=0
            all_marginals.append({'hist_column':hi,'group':g,'R_unchanged':str(rm[g]),'Z_before':str(before[g]),'Z_after':str(znew),'Z_changed':before[g]!=znew})
            # Independently integrate actual R/Z atom bits, not the affine update above.
            masses=defaultdict(F)
            for si in range(slab_start,len(slabs)):
                sg=slabs[si]['groups'];gi=next(k for k,x in enumerate(sg) if group(x)==g)
                for idx in slabs[si]['atom_indices']:
                    atom=atoms[idx];masses[atom['R_bits'][gi],atom['Z_bits'][gi]]+=F(atom['mass'])
            for state,j in st.items():assert masses[state]==new[j]
            assert masses[0,0]==H-sum(new[j] for j in st.values())
        for j,c in enumerate(cols):
            if c['kind']=='overlap' and c['hist_column']==hi:
                g,q=map(group,c['groups']);new[j]=min(rm[g],rm[q]);value=F()
                for si in range(slab_start,len(slabs)):
                    sg=[group(x) for x in slabs[si]['groups']];gi=sg.index(g);qi=sg.index(q)
                    for idx in slabs[si]['atom_indices']:
                        atom=atoms[idx];value+=F(atom['mass'])*atom['R_bits'][gi]*atom['R_bits'][qi]
                assert value==new[j] and new[j]>=weights[j]
        vs=point['variables'][start:len(expected)];ys=[F(v['weight']) for v in vs];bs=[F(v['right'])-F(v['left']) for v in vs]
        assert sum(F(atoms[i]['mass']) for i in atomids)==H
        summary.append({'hist_column':hi,'actual_bits':h['column']['actual_bits'],'hist':h['column']['hist'],'mass':str(H),'groups':len(gs),'R_slabs':len(slabs)-slab_start,'variables':len(vs),'zero':sum(y==0 for y in ys),'upper':sum(y==b for y,b in zip(ys,bs)),'interior':sum(0<y<b for y,b in zip(ys,bs)),'joint_atoms':len(atomids)})
    assert len(expected)==275 and len(slabs)==22
    assert sum(x['zero'] for x in summary)==150 and sum(x['upper'] for x in summary)==104 and sum(x['interior'] for x in summary)==21
    assert point['positive_variables']==125 and point['free_vertex_variables']==21
    assert sum(F(x['mass']) for x in atoms)==F(point['O'])==1
    W=sum(weights[hi] for hi,h in hs.items() if '1' in h['column']['actual_bits']);assert str(W)==point['W']==old['W']
    changed=[j for j,(x,y) in enumerate(zip(weights,new)) if x!=y]
    assert all(cols[j]['kind'] in ('joint-reply','overlap') for j in changed)
    assert all({k:v for k,v in x.items() if k!='weight'}=={k:v for k,v in y.items() if k!='weight'} for x,y in zip(point['variables'],pair['variables'])) and len(pair['variables'])==275
    pair_changed=[i for i,(x,y) in enumerate(zip(point['variables'],pair['variables'])) if F(x['weight'])!=F(y['weight'])]
    zz=prior['all_ZZ_slacks'];assert len(zz)==60 and min(F(z['slack']) for z in zz)==0
    zz_summary=[{'family':f,'query_family':g,'zero':sum(F(x['slack'])==0 for x in zz if (x['family'],x['query_family'])==(f,g)),'positive':sum(F(x['slack'])>0 for x in zz if (x['family'],x['query_family'])==(f,g))} for f,g in product(range(2),repeat=2)]
    report={'status':'PASS_COMPLETE_SPLIT_POINT_AND_COMMON_ATOM_RECONSTRUCTION','sources':[{'path':str(p.relative_to(a.repo)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in [pointpath,oldpath,auditpath,pairpath]],'all_primary_metadata':{k:v for k,v in point.items() if k!='variables'},'source_point_metadata':{k:v for k,v in old.items() if k!='columns'},'histograms':summary,'slabs':slabs,'atoms':atoms,'atom_count':len(atoms),'variable_count':275,'R_slabs':22,'zero_variables':150,'upper_variables':104,'strict_interior_variables':21,'O':str(sum(weights[hi] for hi in hs)),'W':str(W),'one_minus_twice_W':str(1-2*W),'K':str(weights[0]),'reconstructed_old_column_weights':list(map(str,new)),'changed_old_coordinates':changed,'changed_by_kind':dict(Counter(cols[j]['kind'] for j in changed)),'group_marginals':all_marginals,'changed_Z_groups':sum(x['Z_changed'] for x in all_marginals),'changed_R_groups':0,'all_582_joint_and_1306_RR_columns_equal_joint_atom_integrals':True,'existing_ZZ_result_reused':{'new_row_replay':False,'source_sha256':digest(auditpath),'zero':prior['ZZ_zero_rows'],'by_family_pair':zz_summary,'minimum_positive_slack':str(min(F(z['slack']) for z in zz if F(z['slack'])>0))},'pair_successor_comparison':{'rows':pair['rows'],'variables':len(pair['variables']),'same_descriptors':True,'same_W':pair['W']==point['W'],'changed_variable_count':len(pair_changed),'changed_indices':pair_changed,'full_pair_graph_reverified':False},'original_module_imports':0,'graph_builds':0,'LP_calls':0,'scope':'One explicit rational joint membership lift and exact coordinate comparison; no complete strategy, no pair-closure certification and no rerun of existing 60-ZZ integration.'}
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','atom_count','variable_count','changed_by_kind','changed_Z_groups','existing_ZZ_result_reused','pair_successor_comparison']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()

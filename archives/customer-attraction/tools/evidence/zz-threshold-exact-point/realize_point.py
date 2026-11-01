"""Explicit rational membership realization of the frozen 321-variable point.

No author module, graph builder, solver or original verifier is called. Inside
each fixed R slab this chooses one common Z threshold; all old affine moments
are preserved. It certifies membership/moments and the saved 60 ZZ sums, not SPE.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

PAT = tuple(product((0, 1), repeat=3))
EDGES = tuple(e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2])


def group(raw):
    return raw[0], raw[1], tuple(raw[2]), tuple(raw[3])


def pattern(indices):
    seen = {}
    for x in indices:
        if x not in seen:
            seen[x] = len(seen)
    return tuple(seen[x] for x in indices)


def main():
    ap = ArgumentParser()
    ap.add_argument('--source-point', type=Path, required=True)
    ap.add_argument('--candidate', type=Path, required=True)
    ap.add_argument('--prior-audit', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw, candraw = args.source_point.read_bytes(), args.candidate.read_bytes()
    old, candidate = json.loads(raw), json.loads(candraw)
    assert sha256(candraw).hexdigest() == '72b0d89a7c36f304aead4ae0be9fffa7279316870cd6c3070497f19317367bd0'
    assert candidate['source_sha256'] == sha256(raw).hexdigest()
    columns = old['columns']; values = [F(c['weight']) for c in columns]
    assert len(columns) == 1905 and min(values) >= 0
    hists = {}; hi = None
    for j, c in enumerate(columns):
        if c['kind'] == 'hist':
            hi = j; hists[j] = {'column': c, 'groups': {}}
            assert sum(c['hist']) == 6
            assert c['d'] == sum(n*w[0] for n,w in zip(c['hist'],PAT)) == 1
        elif c['kind'] == 'joint-reply':
            states = hists[hi]['groups'].setdefault(group(c['group']), {})
            state = tuple(c['state']); assert state not in states; states[state] = j
    for hi, h in hists.items():
        for states in h['groups'].values():
            assert set(states) == {(0,1),(1,0),(1,1)}
            assert sum(values[j] for j in states.values()) <= values[hi]
    variables = candidate['variables']; masses = [F(v['weight']) for v in variables]
    expected = []; slabs = []; atoms = []; totals = [F() for _ in variables]
    reconstructed = [F() for _ in columns]; reconstructed[0] = values[0]
    summaries = []
    for hi, h in hists.items():
        c, gs, H = h['column'], h['groups'], values[hi]
        words = [w for w,n in zip(PAT,c['hist']) for _ in range(n)]
        edge_groups = [(f,int(i==j),words[i],words[j]) for f,i,j in EDGES]
        assert set(edge_groups) == set(gs)
        rm = {g:values[s[1,0]]+values[s[1,1]] for g,s in gs.items()}
        assert all(0 <= r <= H for r in rm.values())
        begin = len(atoms); sbegin = len(slabs)
        if H:
            cuts = sorted({F(),H,*rm.values()})
            for left,right in zip(cuts,cuts[1:]):
                size = right-left; assert size > 0
                ids, rs = {}, {}
                for g in gs:
                    v = len(expected); ids[g] = v; rs[g] = int(right <= rm[g])
                    desc = {'hist_column':hi,'left':str(left),'right':str(right),
                            'group':[g[0],g[1],list(g[2]),list(g[3])],'r':rs[g]}
                    assert {k:x for k,x in variables[v].items() if k != 'weight'} == desc
                    expected.append(desc); assert 0 <= masses[v] <= size
                localcuts = sorted({F(),size,*(masses[v] for v in ids.values())})
                slab_index = len(slabs)
                slabs.append({'hist_column':hi,'left':str(left),'right':str(right),
                              'variables':list(ids.values()),'local_Z_thresholds':[str(x) for x in localcuts]})
                for a,b in zip(localcuts,localcuts[1:]):
                    weight = b-a; assert weight > 0
                    zs = {g:int(b <= masses[v]) for g,v in ids.items()}
                    bits = list(map(int,c['actual_bits']))
                    bits += [w[k] for k in range(3) for w in words]
                    bits += [rs[g] for g in edge_groups]+[zs[g] for g in edge_groups]
                    assert len(bits)==156
                    atoms.append({'hist_column':hi,'R_slab':slab_index,'Z_left':str(a),'Z_right':str(b),
                                  'mass':str(weight),'membership_156':''.join(map(str,bits))})
                    reconstructed[hi] += weight
                    for g,states in gs.items():
                        state = (rs[g],zs[g]); j = states.get(state)
                        if j is not None:
                            reconstructed[j] += weight
                        if zs[g]:
                            totals[ids[g]] += weight
                    for j,col in enumerate(columns):
                        if col['kind']=='overlap' and col['hist_column']==hi:
                            g,f = map(group,col['groups'])
                            reconstructed[j] += weight*rs[g]*rs[f]
        summaries.append({'hist_column':hi,'mass':str(H),'groups':len(gs),
                          'R_slabs':len(slabs)-sbegin,'membership_atoms':len(atoms)-begin})
    assert len(expected)==len(variables)==candidate['variables_count']==321
    assert totals == masses
    assert sum(x>0 for x in masses)==candidate['positive_variables']==134
    interior = sum(F(0)<m<F(v['right'])-F(v['left']) for m,v in zip(masses,variables))
    assert interior==candidate['free_vertex_variables']==17
    old_new_groups = []
    for hi,h in hists.items():
        assert reconstructed[hi]==values[hi]
        H=values[hi]
        for g,s in h['groups'].items():
            oldr = values[s[1,0]]+values[s[1,1]]
            newr = reconstructed[s[1,0]]+reconstructed[s[1,1]]
            oldz = values[s[0,1]]+values[s[1,1]]
            newz = reconstructed[s[0,1]]+reconstructed[s[1,1]]
            assert oldr==newr
            zero = H-sum(reconstructed[j] for j in s.values()); assert zero>=0
            old_new_groups.append({'hist_column':hi,'group':[g[0],g[1],list(g[2]),list(g[3])],
                                   'R_mass':str(oldr),'old_Z_mass':str(oldz),'new_Z_mass':str(newz),
                                   'new_00':str(zero),'new_01':str(reconstructed[s[0,1]]),
                                   'new_10':str(reconstructed[s[1,0]]),'new_11':str(reconstructed[s[1,1]])})
    for j,c in enumerate(columns):
        if c['kind']=='overlap':
            gs=hists[c['hist_column']]['groups']
            r=[sum(values[gs[group(g)][s]] for s in [(1,0),(1,1)]) for g in c['groups']]
            assert reconstructed[j]==min(r)
    patterns=sorted({pattern(x) for x in product(range(4),repeat=4)})
    zz={(f,g,p):F() for f,g,p in product(range(2),range(2),patterns)}
    for atom in atoms:
        bits=list(map(int,atom['membership_156'])); mass=F(atom['mass']); p=sum(bits[:4])
        R,Z=bits[24:90],bits[90:156]
        for ei,(f,i,j) in enumerate(EDGES):
            for fi,(g,k,l) in enumerate(EDGES):
                zz[f,g,pattern((i,j,k,l))] += mass*F(Z[ei]-Z[fi],p+1+R[ei])
    prior=json.loads(args.prior_audit.read_text())['modes']['default']
    priorzz={(r['family'],r['query_family'],tuple(r['equality_pattern'])):F(r['slack']) for r in prior['all_ZZ_slacks']}
    assert zz==priorzz and min(zz.values())==0
    O=sum(F(a['mass']) for a in atoms)
    W=sum(F(a['mass']) for a in atoms if '1' in a['membership_156'][:6])
    assert O==F(candidate['O'])==1 and W==F(candidate['W'])==F(old['W'])<F(1,2)
    assert all('1' in a['membership_156'][6:12] for a in atoms)
    changes=[{'column':j,'kind':c['kind'],'old':str(values[j]),'new':str(reconstructed[j])}
             for j,c in enumerate(columns) if values[j]!=reconstructed[j]]
    labels=[f'A{i+1}' for i in range(6)]+[f'{s}{i+1}' for s in ['T','B','C'] for i in range(6)]
    labels += [f'{s}{f}_{i+1}_{j+1}' for s in ['R','Z'] for f,i,j in EDGES]
    output={'status':'PASS_EXPLICIT_COMMON_MEMBERSHIP_AND_SAVED_MOMENTS',
            'source_sha256':sha256(raw).hexdigest(),'candidate_sha256':sha256(candraw).hexdigest(),
            'auditor_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'prior_ZZ_audit_sha256':sha256(args.prior_audit.read_bytes()).hexdigest(),
            'variables_checked':len(variables),'positive_variables':134,'strict_interior_variables':interior,
            'histograms':len(hists),'positive_histograms':sum(values[j]>0 for j in hists),
            'R_slabs':len(slabs),'positive_membership_atoms':len(atoms),'theme_labels':labels,
            'histogram_summary':summaries,'slabs':slabs,'atoms':atoms,
            'all_321_Z_masses_reconstructed':True,'all_194_R_marginals_preserved':True,
            'all_1306_RR_intersections_equal_min':True,'joint_groups':old_new_groups,
            'Z_marginals_changed':sum(r['old_Z_mass']!=r['new_Z_mass'] for r in old_new_groups),
            'reconstructed_1905_weights':[str(x) for x in reconstructed],
            'changed_columns_by_kind':dict(Counter(r['kind'] for r in changes)),'changed_columns':changes,
            'O':str(O),'W':str(W),'half_gap':str(1-2*W),
            'all_60_ZZ_equal_prior_exact_audit':True,'zero_ZZ_rows':sum(v==0 for v in zz.values()),
            'ZZ_rows':[{'family':f,'query_family':g,'pattern':list(p),'slack':str(v)} for (f,g,p),v in zz.items()],
            'original_program_calls':0,'LP_calls':0,'old_3889_rows_regenerated':False,
            'limits':'One common membership completion using nested Z inside fixed R slabs; no strategy or SPE, no independent rebuild of 3889 old graph rows, no vertex rank or optimum proof. Hist atoms use canonical sorted comparison words; indexed strategy constraints are not separately certified.'}
    args.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ['theme_labels','histogram_summary','slabs','atoms','joint_groups','reconstructed_1905_weights','changed_columns','ZZ_rows']},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()

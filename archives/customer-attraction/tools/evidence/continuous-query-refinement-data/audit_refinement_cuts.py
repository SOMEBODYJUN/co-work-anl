"""Audit all 32 frozen refinement cuts at four distinct finite stage points.

Reuses the already archived mathematical integration helper, never the old
generator or an LP. A separate original entry event checks all 5075 rows.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy
import sys

HERE = Path(__file__).resolve().parent
EV = HERE.parent
CUTS = EV/'continuous-old-query-cut-data/related/continuous_refinement_cuts.json'
PREVIOUS = EV/'continuous-old-query-cut-data/original/continuous_old_query_cuts.json'
INTEGRATOR = EV/'continuous-old-query-cut-data/audit_cuts.py'
REFINED = EV/'continuous-query-refinement-program/related/continuous_refinement_exact.json'
EXPECTED = {
    CUTS: 'aa696d0ebbb1e5b1ccc3b593c5f5a4bcac4cf411966dfd9499192d8170fb5c36',
    PREVIOUS: 'e9ce9c66ea5598038ad7f5aa19cfab44d5156c8e35b3081665481153a968c4fa',
    REFINED: 'abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246',
}


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    for path, sha in EXPECTED.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
    definitions = runpy.run_path(str(INTEGRATOR),run_name='shared_mathematical_definitions')
    for path, sha in definitions['EXPECTED'].items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
    data = json.loads(CUTS.read_text())
    assert set(data) == {'scope','cuts'}
    cuts = data['cuts']
    assert len(cuts) == len({tuple(c) for c in cuts}) == 32
    for cut in cuts:
        assert len(cut) == 8
        i,m,f,d,q,am,al,mu = cut
        assert i in range(5) and m in (0,1) and (f,d) in ((0,0),(1,0),(1,1)) and q in range(6)
        assert all(isinstance(x,str) and F(x)>=0 for x in (am,al,mu))
    old64 = [tuple(r['cut']) for r in json.loads(PREVIOUS.read_text())['selected']]
    cset = {tuple(c) for c in cuts}
    point_paths = {'old_4971':definitions['OLD'], 'refined_5075':REFINED,
                   'combined_5108':definitions['MASTER']}
    stages, point_reading = {}, {}
    for name,path in point_paths.items():
        point = json.loads(path.read_text())
        hs = definitions['read_point'](point)
        assert len(point['columns']) == 1905
        assert sum(h['mass'] for h in hs.values()) == 1
        assert all(sum(n*w[0] for n,w in zip(h['hist'],definitions['PAT']))==1 for h in hs.values())
        welfare = sum((h['mass'] for h in hs.values() if any(h['a'])),F())
        assert welfare == F(point['W'])
        point_reading[name] = {'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                              'bytes':path.stat().st_size,'columns':len(point['columns']),
                              'positive_columns':sum(F(c['weight'])>0 for c in point['columns']),
                              'histograms':len(hs),'O':'1','W':str(welfare),
                              'author_verified_rows':point['verified_rows']}
        stages[name] = [definitions['evaluate'](hs,c) for c in cuts]
    pair_hs = definitions['read_point'](json.loads(definitions['MASTER'].read_text()))
    pair = json.loads(definitions['PAIR'].read_text())
    zmass = {}
    for c in pair['variables']:
        k = c['hist_column'], definitions['key'](c['group'])
        zmass[k] = zmass.get(k,F())+F(c['weight'])
    for hi,h in pair_hs.items():
        for g,values in h['marginals'].items():
            values[1] = zmass.get((hi,g),F())
    stages['changed_Z_pair'] = [definitions['evaluate'](pair_hs,c) for c in cuts]
    assert all(v<0 for v in stages['old_4971'])
    assert all(v>=0 for name,vs in stages.items() if name!='old_4971' for v in vs)
    summaries = {name:{'rows':len(vs),'negative':sum(v<0 for v in vs),'zero':sum(v==0 for v in vs),
                       'positive':sum(v>0 for v in vs),'minimum':str(min(vs)),'maximum':str(max(vs))}
                 for name,vs in stages.items()}
    raw_master = json.loads(definitions['MASTER'].read_text())['columns']
    raw_refined = json.loads(REFINED.read_text())['columns']
    descriptors_equal = all({k:v for k,v in a.items() if k!='weight'}=={k:v for k,v in b.items() if k!='weight'}
                            for a,b in zip(raw_master,raw_refined))
    assert descriptors_equal
    weights_different = sum(F(a['weight'])!=F(b['weight']) for a,b in zip(raw_master,raw_refined))
    assert weights_different>0
    return {'status':'PASS_ALL_32_CUTS_EXACT_FOUR_STAGE_EVALUATION',
            'scope':'Complete two-field frozen table and all 32 eight-coordinate records; finite cut evaluation. Not adaptive-discovery replay or all other rows at changed Z.',
            'python_version':sys.version,
            'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'mathematical_integrator_sha256':hashlib.sha256(INTEGRATOR.read_bytes()).hexdigest(),
            'source_sha256':{str(p.relative_to(EV)):sha for p,sha in EXPECTED.items()},
            'original_scope':data['scope'],'record_count':32,
            'coordinate_counts':{name:dict(Counter(str(c[j]) for c in cuts)) for j,name in enumerate(
                ('source_index','member','family','diagonal','query_bit','alpha_middle','alpha_last','mu'))},
            'old64_comparison':{'exact_tuple_intersection':len(cset&set(old64)),
                                'only_in_refinement':sorted(cset-set(old64)),
                                'overlap_with_old_first32':len(cset&set(old64[:32])),
                                'only_tuple_difference_not_linear_independence':True},
            'point_reading':point_reading,'refined_and_combined_descriptors_equal':descriptors_equal,
            'refined_and_combined_weight_positions_different':weights_different,
            'refined_and_combined_W_equal':point_reading['refined_5075']['W']==point_reading['combined_5108']['W'],
            'stage_summaries':summaries,
            'all_32_rows':[{'position':j,'cut':cut,**{name:str(vs[j]) for name,vs in stages.items()}}
                           for j,cut in enumerate(cuts)],
            'not_certified':['historical adaptive iterations or LP choices','continuous family closure',
                             'exact optimum','all 5108/10344 rows at changed Z','complete-history SPE']}


if __name__ == '__main__':
    report = run()
    (HERE/'four-stage-cut-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

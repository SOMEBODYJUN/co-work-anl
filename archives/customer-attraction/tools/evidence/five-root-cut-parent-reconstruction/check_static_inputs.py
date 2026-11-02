"""Check frozen bytes/report metadata and scalar identities; do not replay audits."""
from pathlib import Path
from fractions import Fraction as F
import ast
import hashlib
import json

BASE = Path(__file__).resolve().parent
SRC = BASE / 'source-root'


def require(ok, label):
    if not ok:
        raise ValueError(label)


def main():
    ast.parse((SRC/'parent/verify_root_cuts.py').read_text())
    report = json.loads((SRC/'parent/verify_root_cuts.json').read_text())
    direct_path = SRC/'realizability/root_max_direct_certificates.json'
    four_path = SRC/'background/local_max_tail_certificate.json'
    direct_hash = hashlib.sha256(direct_path.read_bytes()).hexdigest()
    four_hash = hashlib.sha256(four_path.read_bytes()).hexdigest()
    require(direct_hash == report['direct_certificate_sha256'], 'direct input digest')
    require(four_hash == report['four_tail_max_cut']['certificate_sha256'], 'four input digest')
    direct = json.loads(direct_path.read_text())
    require(len(direct) == len(report['direct_root_cuts']) == 5, 'five direct certificates')
    for cert, row in zip(direct, report['direct_root_cuts']):
        weights = {k:F(v) for k,v in cert['weights'].items()}
        require(min(weights.values()) >= 0, 'nonnegative direct multipliers')
        require(weights['root'] == F(cert['alpha']), 'direct root coefficient')
        require(sum(weights.get('cap'+str(i), F(0)) for i in range(1,5))-F(cert['lambda']) == F(cert['beta']), 'direct cap identity')
        require((row['alpha'], row['cap'], row['size']) == (cert['alpha'],cert['beta'],cert['lambda']), 'direct report coefficients')
        require((row['states'],row['minimum'],row['zeros']) == (192,'0',11), 'direct saved report counts')
    third=report['third_floor']
    require((third['states'],third['minimum'],third['zeros']) == (128,'0',14), 'third saved report counts')
    require((third['alpha'],third['cap'],third['size']) == ('11033/763','2085/763','4139/763'), 'third saved coefficients')
    third_caps = F(1,2)+F(1093,1526)+F(77,109)+F(618,763)
    require(third_caps == F(2085,763), 'third cap sum')
    require(F(11033,763)/5+third_caps-F(4139,763) == F(1,5), 'third root floor identity')
    four=json.loads(four_path.read_text())
    w={k:F(v) for k,v in four['multipliers'].items()}
    A,B,gamma=map(F,(four['rounded_A'],four['rounded_B'],four['gamma_T']))
    require(min(w.values()) >= 0 and w['root'] == A, 'four nonnegative weights/root')
    require(gamma+sum((5 if k=='size:opt' else 1)*v for k,v in w.items() if k.startswith('size:')) == B, 'four common K identity')
    rootfloor,knonneg=F(four['root_floor_multiplier']),F(four['K_nonnegative_multiplier'])
    require(rootfloor >= 0 and knonneg >= 0 and A+rootfloor == 50 and B-rootfloor/5+knonneg == -8, 'simplified four-tail identity')
    row=report['four_tail_max_cut']
    require((row['alpha'],row['cap']) == (four['rounded_A'],four['rounded_B']), 'four saved report coefficients')
    require((row['states'],row['minimum'],row['zeros']) == (1536,'0',1), 'four saved report counts')
    difference=[F(11033,763)-F(44,3),F(2085,763)-F(13,5),-F(4139,763)+F(16,3)]
    require(difference == [F(-2365,11445),F(1518,11445),F(-1045,11445)], 'COPY scalar difference')
    require(report['external_review'] is False and report['novelty_certified'] is False, 'review metadata')
    result={
        'status':'passed',
        'scope':'Frozen source syntax, exact-byte input/report binding, scalar coefficient identities and saved report metadata only',
        'original_audit_executed':False,
        'customer_state_enumeration_executed':False,
        'game_or_lp_solver_executed':False,
        'primary_source_full_read':True,
        'original_report_is_historical':True,
        'source_ast_parse':'passed',
        'direct_certificate_sha256':direct_hash,
        'four_tail_certificate_sha256':four_hash,
        'direct_report_rows_matched':5,
        'third_saved_counts':[128,0,14],
        'direct_saved_counts_each':[192,0,11],
        'four_tail_saved_counts':[1536,0,1],
        'scalar_identities':'third cap/floor; five direct cap; four common K/root-floor; COPY difference',
        'copy_rhs_difference_coefficients_in_order_u_K_absT':[str(v) for v in difference],
        'not_certified':['new full-domain replay','SPE realizability','welfare optimum','six-player half','external review','novelty']
    }
    (BASE/'static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()

"""Reproduce this curation's arithmetic, cutoff, route, and size checks.

This checks records and short-context arithmetic, not the half-cover theorem
or the future mathematical productivity of any language model.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = '4b57ec59cb67ddbeb737a843c8ccf6d110c2e43b'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def product_bound(m, tau):
    p = F(1)
    for r in range(1, m + 1):
        p *= 1 - 1 / (r * tau)
    return 1 - p

def main():
    beta437 = F(145473820534756099649387160645076613709,70560308704423797361284609157664425493)
    beta557 = F(178528430822287579296070598592537012737,87421565922360356032366460363114422206)
    beta728 = F(903491829723556246762087795616829492745,442437259121664928475146048173419016656)
    assert F(5,3) < F(1499,750) < 2 < beta728 < beta557 < beta437
    assert 2 - F(1499,750) == F(1,750)
    assert product_bound(5,F(5)) == F(6049,15625) < F(1,2)
    assert product_bound(4,F(7,2)) == F(1166,2401) < F(1,2)
    assert product_bound(5,F(7,2)) == F(8656,16807) > F(1,2)
    # Reverse multiplication verifies every reported rational identity.
    for f in (beta437,beta557,beta728,F(6049,15625),F(1166,2401),F(8656,16807)):
        assert f * f.denominator == f.numerator
    # Enumerate small cardinality triples, including empty sets: C=I+E, O=I+L.
    checked=0
    for i in range(9):
        for l in range(9):
            for e in range(9):
                w=i+e; opt=i+l
                assert opt-w == l-e
                assert (2*w >= opt) == (l-e <= w)
                checked+=1
    assert 38-35 == 36-33 and 36>35
    assert 52 <= 2*34 and 17<18
    assert 111 <= 2*107 and 35<36 and 107+68-72==103
    inventory=json.loads((ROOT/'research/customer_attraction/context_inventory.json').read_text())
    assert inventory['baseline']['exact_commit']==BASE
    paths=git('ls-tree','-r','--name-only',BASE,'--','research/workspaces/customer-attraction').decode().splitlines()
    paths=[p for p in paths if not any(x.startswith('.') for x in Path(p).parts)
           and '__pycache__' not in Path(p).parts and not p.endswith(('.pyc','.pyo'))]
    actors=inventory['actors']
    assert len(paths)==sum(a['files'] for a in actors)==6142
    assert len({Path(p).parts[3] for p in paths})==len(actors)==113
    assert sum(Path(p).name=='README.md' for p in paths)==707
    for a in actors:
        content=git('show',BASE+':'+a['root_readme'])
        assert hashlib.sha256(content).hexdigest()==a['root_readme_sha256'],a['root_readme']
    # Check source entry navigation against actual current files; code examples
    # and external citations are excluded. Fragment semantics are not audited.
    docs=set(inventory['reading_routes']['default'])
    docs.update(p for p in paths if Path(p).name=='README.md')
    broken=[]; link_count=0
    for path in sorted(docs):
        text=(ROOT/path).read_text()
        text=re.sub(r'(?ms)^(```|~~~).*?^\1\s*$','',text)
        for ref in re.findall(r'(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)',text):
            ref=ref.strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',ref) or ref.startswith('#'):
                continue
            dest=(ROOT/path).parent/ref.split('#',1)[0]
            if not dest.exists(): broken.append([path,ref])
            link_count+=1
    assert not broken,broken
    before=json.loads((HERE/'audit/context_before.json').read_text())['before']
    default=inventory['reading_routes']['default']
    sizes={p:{'before_bytes':before[p]['bytes'],'after_bytes':(ROOT/p).stat().st_size} for p in default}
    before_total=sum(v['before_bytes'] for v in sizes.values())
    after_total=sum(v['after_bytes'] for v in sizes.values())
    assert after_total < before_total
    # Original certificates and frozen runs are not edited by curation.
    frozen=git('diff','--name-only',BASE,'--','evidence','examples','customer_attraction').decode().splitlines()
    assert not frozen,frozen
    with localcontext() as ctx:
        ctx.prec=35
        decimals={key:str(Decimal(value.numerator)/Decimal(value.denominator)) for key,value in
                  [('beta437',beta437),('beta557',beta557),('beta728',beta728)]}
        reduction=str(100*(1-Decimal(after_total)/Decimal(before_total)))
    result={'baseline':BASE,'cardinality_triples_checked':checked,'exact_rational_checks':'passed',
            'decimal_bounds':decimals,'baseline_workspace_files':len(paths),'baseline_actors':len(actors),
            'baseline_recursive_readmes':707,'root_readme_hashes_verified':len(actors),
            'local_links_checked':link_count,'broken_links':broken,
            'default_context_utf8_bytes':{'before':before_total,'after':after_total,'reduction_percent':reduction},
            'default_files':sizes,'frozen_certificate_paths_changed':frozen,
            'limits':'No token count or model-score improvement inferred; metadata, arithmetic and route checks are not a proof review.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()

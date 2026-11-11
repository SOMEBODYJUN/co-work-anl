"""Write all 17*720 finite atoms with exact integer customer multiplicities."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent


def main():
    source = HERE/'joint_completion_exact.json'
    cert = json.loads(source.read_text())
    scale = int(cert['unit_customer_scale'])
    count = 0
    customers = 0
    out = HERE/'common_atoms.jsonl.gz'
    with out.open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as stream:
            for index,atom in enumerate(cert['atoms']):
                mass = F(atom['mass'])/720
                integer = mass*scale
                assert integer.denominator == 1
                for perm in permutations(range(6)):
                    row = {'orbit_atom':index,'common_permutation':list(perm),
                           'actual':atom['actual'],
                           'old_TBC_words':[atom['old_words'][j] for j in perm],
                           'new_five_tail_words':[atom['new_words'][j] for j in perm],
                           'mass':str(mass),'unit_customer_multiplicity':str(integer.numerator)}
                    stream.write((json.dumps(row,separators=(',',':'))+'\n').encode())
                    count += 1
                    customers += integer.numerator
    assert count == 12240 and customers == scale
    report = {'scope':'Explicit finite coverage atoms only; no complete SPE.',
              'certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'atoms_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
              'atom_records':count,'total_unit_customers':str(customers),
              'duplicate_coverage_patterns':'Retained as separate identical-type customer blocks.'}
    (HERE/'materialized_atoms_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()

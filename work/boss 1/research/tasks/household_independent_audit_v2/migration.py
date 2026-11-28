"""Migrate only newly introduced optional contract terms in the earlier synthetic audit.

Old limits were unrestricted by construction for fully specified, prepayment-enabled
contracts. Sparse or expressly prohibited contracts retain their original uncertainty.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL_REPORT = HERE.parent / 'household_independent_audit'
OLD_INPUT_HASH = '3e0f3157af50ea21873a8fa1777c4c32ac92e29d0ac7bd97f58f80c5c8a8a991'
OLD_RECEIPT_HASH = '1e37a9a574b155abc1dbf71da21433c3c3ac47e423389b9e527585d5d5420ffc'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def explicit_terms(secured=False):
    return {
        'allowFull': True, 'prepayMax': 'unlimited', 'prepayPeriodMax': 'unlimited',
        'prepayPeriodMonths': None, 'prepayPeriodRemaining': None, 'prepayPeriodUsed': None,
        'salePayoffRule': 'same_terms' if secured else 'unknown',
        'salePayoffFrom': None, 'salePayoffFee': None, 'saleSettlementFee': None,
        'salePayoffFeeBase': 'balance' if secured else 'unknown',
        'saleMaturityReleaseFee': 'in_asset_cost' if secured else None,
    }


def migrate_generated(originals, save=False):
    original_bytes = (HERE / 'original_input.json').read_bytes()
    old_receipt = (ORIGINAL_REPORT / 'engine_receipt.json').read_bytes()
    assert sha(original_bytes) == OLD_INPUT_HASH
    assert originals == json.loads(original_bytes)
    assert sha(old_receipt) == OLD_RECEIPT_HASH
    assert all(sha((ORIGINAL_REPORT / f).read_bytes()) == expected
               for f, expected in json.loads(old_receipt)['artifacts'].items())
    migrated = [deepcopy(request) for request in originals]
    diff = []
    skipped = []
    for source, target in zip(originals, migrated):
        if source['household'] is None:
            continue
        for i, loan in enumerate(source['household']['loans']):
            # Test Q is deliberately a sparse contract. Preserve it exactly even in
            # the variant where generic early prepayment was enabled but fees were absent.
            if loan.get('canPrepay') is not True or loan.get('prepayFrom') is None:
                skipped.append({'case': source['id'], 'loan': loan['id'],
                                'reason': 'original prohibition or intentionally sparse loan'})
                continue
            new_fields = explicit_terms(bool(loan.get('collateral')))
            assert not set(new_fields).intersection(loan)
            target['household']['loans'][i].update(new_fields)
            diff.append({'case': source['id'], 'path': f'/household/loans/{i}', 'loan': loan['id'],
                         'old': 'all these fields absent', 'added': new_fields})
    restored = deepcopy(migrated)
    by_id = {r['id']: r for r in restored}
    for patch in diff:
        i = int(patch['path'].rsplit('/', 1)[1])
        contract = by_id[patch['case']]['household']['loans'][i]
        for k in patch['added']:
            del contract[k]
    assert restored == originals
    if save:
        notes = {
            'oldInputSha256': OLD_INPUT_HASH, 'oldReceiptSha256': OLD_RECEIPT_HASH,
            'allOldReceiptArtifactHashesVerified': True,
            'oldPolicyMeaning': 'Fully specified, explicitly prepayment-enabled synthetic loans previously had no cumulative or per-action cap. Exact opening balance was the sale fee basis. The ordinary contract governed secured sale. These assumptions belong only to these artificial checks.',
            'inactiveFields': 'Explicit null marks fields inapplicable to the stated unlimited periodic quota and disabled separate sale exception. No period length, usage history or independent sale waiver was invented.',
            'scope': 'Only the listed newer keys were added. Removing the patch reproduces every old record exactly, including the explicit scenario targets, ordinary contract schedules and all household amounts.',
            'unchangedRequests': len(originals)-len({p['case'] for p in diff}),
            'patchedCases': len({p['case'] for p in diff}), 'patchedLoans': len(diff),
            'addedFieldsByCase': diff, 'loansLeftUnchanged': skipped,
        }
        (HERE / 'migration_diff.json').write_text(json.dumps(notes, indent=2, ensure_ascii=False)+'\n')
    return migrated

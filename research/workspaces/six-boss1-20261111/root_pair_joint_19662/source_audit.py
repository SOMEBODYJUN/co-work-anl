"""Bind already-read mathematical sources and the exact registered identities."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    registrations = json.loads((REPO/'research/registry.json').read_text())['objects']
    if isinstance(registrations, dict):
        registrations = list(registrations.values())
    objects = {r['object_id']: r for r in registrations}
    uses = {
        'M-e960d7f4ebca40a38760eb3ae044cc19': {
            'role': 'Direct mathematical premise.',
            'conditions_used': 'Same complete pure SPE, any legal ordered background, exactly two remaining players, arbitrary legal possibly repeated or empty query labels; three true ICs and one nonnegative overlap remainder.',
            'does_not_supply': 'No arbitrary membership completion theorem, no SPE sufficiency, and no general half theorem.',
            'observed_show_version': 2,
            'observed_show_registration_pin': 'ab054800337d5944cb152e30ad29e8398e6cb46284ce218ad99be5485c5c3406',
        },
        'customer-attraction/actual-prefix-whole-catalog-one-step-deviation-rows': {
            'role': 'Premise for the retained SAFE rows.',
            'conditions_used': 'The true source payoff, actual ordered source prefix, and remaining number of players; the deviation follows the same original strategy.',
            'does_not_supply': 'No replacement of an off-path source payoff by an actual payoff.'},
        'customer-attraction/ordered-middle-safe-joint-tail-projection': {
            'role': 'Premise for joint membership and global multiplier interpretation.',
            'conditions_used': 'Keep the complete ordered tail and shared topic memberships, sum all source/price/capacity/SAFE costs before minimizing, with customer-independent nonnegative weights.',
            'does_not_supply': 'No separate minimization after cross-branch queries have coupled the blocks.'},
        'M-e394b173b9b1419588c6c380da4bd326': {
            'role': 'Closest related cross-branch joint-PAIR object; not used to transplant its special coefficients.',
            'conditions_used': 'Its shared-topic, same-donor overlap and joint-before-min principle are compatible with the current construction.',
            'does_not_supply': 'Its two forced branches return to one identical ordered source. The present old branch and new root branch have different source histories, so its nine-row formula and source-payment normalization are not imported.',
            'observed_show_version': 1,
            'observed_show_registration_pin': 'c086b2c45d91b3ecb2886ded949f98d9c129852119639f0280e1a903f3dc79d7',
        },
    }
    selected = []
    for key, use in uses.items():
        record = objects[key]
        body = record['body']
        assert sha(REPO/body['path']) == body['sha256']
        selected.append({'object_id': key, 'version': record['version'],
            'body': body, 'body_binding': 'current at this exact read',
            'statement': record['statement'], 'quantifiers': record['quantifiers'],
            'assumptions': record.get('assumptions', []), 'scope': record['scope'], **use})
    sources = [
        ('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
         'Full text read; retain labelled catalog, all ordered histories, exact six players, unit customers, ties, repetitions, empty coverage and zero customers.'),
        ('archives/customer-attraction/state/引理/固定背景两人税界--引理.md',
         'Full text read; ordinary two-player tax contrasted with the stronger retained-overlap identity.'),
        ('archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md',
         'Full text read directly and through current registered show --body. Three true ICs derive every new pair row.'),
        ('archives/customer-attraction/state/引理/真实前缀全目录单步偏离行--引理.md',
         'Full text read for true source safety and off-path payoff scope.'),
        ('archives/customer-attraction/state/引理/真实中间玩家安全行的联合尾会员投影--引理.md',
         'Full text read for shared tail memberships and global fixed nonnegative multipliers.'),
        ('archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md',
         'Full registered body read; related object only, with distinct source-history conditions explicitly preserved.'),
        ('research/workspaces/six-boss1-20261111/root_early_tail28.md',
         'Full text read, including section 7 specifying this next 36-row obligation. Its old-point masses and signs are not transferred.'),
        ('research/workspaces/six-boss1-20261111/root_old_tail_joint.md',
         'Full text read; complete finite incidence domain and joint old-word requirements.'),
        ('research/workspaces/six-boss1-20261111/root_old_tail_joint/verify_completion.py',
         'Full source read as audit reference; never imported or executed by the new verifier.'),
        ('research/workspaces/six-boss1-20261111/root_early_tail28/verify_completion.py',
         'Full source read as audit reference; previous giant permutation-query loop was not rerun.'),
        ('research/workspaces/six-boss1-20261111/cross_root_pricing.md',
         'Full text read; original 163 budgets, common roots and root-source coefficient 1.'),
        ('research/workspaces/six-boss1-20261111/cross_root_pricing/contract.py',
         'Full source read; constructor reuses this read-only root coefficient implementation, while the verifier imports none of it.'),
        ('research/workspaces/six-boss1-20261111/background_five_bridge.md',
         'Sections 1-3.2 read for physical background, true two-player tax and original fixed remainder provenance; no large 53-row recomputation.'),
        ('research/workspaces/six-boss1-20261111/background_root_bridge.md',
         'Sections 5-8 read in relevant supplied segments for root source average, ROOT-71 budgets and its previous finite nonseparation scope.'),
        ('research/GITHUB_RESOURCES.md',
         'Full text read. No cloud request was needed after the small exact completion succeeded.'),
        ('research/workspaces/six-boss1-20261111/main_19662_audit.json',
         'Full audit read and bound. Main supplies the 19662-row exact matrix audit; this task does not repeat the global matrix audit.'),
    ]
    report = {'scope': 'Read-only source binding for this new-point application; no registration edits.',
        'actual_argv': [sys.executable, *sys.argv], 'script_sha256': sha(__file__),
        'registered_objects': selected,
        'sources': [{'path': p, 'sha256': sha(REPO/p), 'use': use} for p, use in sources],
        'lookup_note': 'The frontmatter id customer-attraction/two-tail-overlap-and-index-aggregation is not the registry key. The exact current registered key was resolved to M-e960d7f4ebca40a38760eb3ae044cc19 and opened with --body.'}
    (HERE/'source_reading.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'registered_objects': [{'object_id': r['object_id'], 'version': r['version'],
        'body_sha256': r['body']['sha256']} for r in selected], 'source_files_bound': len(sources)}, indent=2))


if __name__ == '__main__':
    main()

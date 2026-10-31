from pathlib import Path
import hashlib, json

base = Path(__file__).resolve().parent.parent
source = base / 'source' / 'code_bank_suffix_probe.json'
generated = base / 'replay' / 'generated.json'
script = base / 'source' / 'inspect_code_bank.py'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(source) == '829cc98c9244e4c0999a6e77a08d96893b15aa89449a7cb8ae847ca9ca294a1b'
assert sha(script) == 'e9d908fd848b6d5cf2f7eede9fe454fbf65578f7256848a20ca8ea71539e584c'
assert source.read_bytes() == generated.read_bytes()
rows = json.loads(source.read_text())
assert len(rows) == 4
expected = [(2,1,1,False,'18','39/2',1,165,120,165),
            (3,1,1,False,'27','57/2',3,969,816,1005),
            (3,2,3,True,'54','58',4,969,816,1005),
            (4,1,1,True,'36','75/2',12,6545,5984,6996)]
for row, exp in zip(rows, expected):
    d,x,y,shared,u,t,checked,states,terminal,retained=exp
    assert (row['d'],row['x'],row['y'],row['shared_omissions'],row['desired_loader_payoff'],row['true_threshold'],row['Bj_continuations_checked']) == (d,x,y,shared,u,t,checked)
    assert (row['stats']['count_states'],row['stats']['terminal_states'],row['stats']['retained_outcomes']) == (states,terminal,retained)
    assert row['desired_in_outcomes'] is False
    assert row['all_true_last_rows_pass'] and row['all_frozen_loader_rows_pass'] and row['all_Bj_continuations_bank_balanced']
    actions = {a['action']: a for a in row['actions']}
    assert all(a['exceeds_desired'] for name,a in actions.items() if name.startswith('B'))
    assert all(not a['exceeds_desired'] for name,a in actions.items() if not name.startswith('B'))
print('PASS')

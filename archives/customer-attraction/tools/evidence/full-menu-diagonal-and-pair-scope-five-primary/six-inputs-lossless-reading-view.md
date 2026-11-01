
# portfolio_matching_failure
DATA: {"topics": ["A", "B", "T", "D", "E"], "customers": [{"topics": [0], "multiplicity": 15}, {"topics": [1], "multiplicity": 15}, {"topics": [0, 2], "multiplicity": 6}, {"topics": [1, 2], "multiplicity": 5}, {"topics": [0, 1, 2], "multiplicity": 1}, {"topics": [3], "multiplicity": 16}, {"topics": [2, 3], "multiplicity": 6}, {"topics": [4], "multiplicity": 14}, {"topics": [2, 4], "multiplicity": 6}, {"topics": [1, 2, 4], "multiplicity": 2}], "players": 2}
UNIT CUSTOMER COUNT: 86
CERTIFICATE NON-ACTION FIELDS: {"terminal_counts": [1, 0, 0, 0, 1]}
STRATEGY NON-ACTION FIELDS: {"terminal_counts": [1, 0, 0, 0, 1]}
root: 4
depth 1; for each lex prefix, digit j gives prescribed action at prefix+(j,)
root:12120
STRUCTURE ONLY: {"all_actions_unique": true, "exact_complete_history_keys": true, "all_labels_legal": true, "action_rows": 6}

# root_tax_failure
DATA: {"topics": ["A", "B", "C", "D", "E", "F"], "players": 4, "customers": [{"topics": [0], "multiplicity": 12}, {"topics": [1], "multiplicity": 8}, {"topics": [2], "multiplicity": 4}, {"topics": [3], "multiplicity": 8}, {"topics": [0, 4], "multiplicity": 6}, {"topics": [0, 5], "multiplicity": 6}, {"topics": [2, 4], "multiplicity": 3}, {"topics": [2, 5], "multiplicity": 3}, {"topics": [0, 4, 5], "multiplicity": 6}, {"topics": [1, 4, 5], "multiplicity": 2}, {"topics": [2, 4, 5], "multiplicity": 1}, {"topics": [3, 4, 5], "multiplicity": 2}]}
UNIT CUSTOMER COUNT: 61
CERTIFICATE NON-ACTION FIELDS: {"claim": "CA-ROOT-TAX-NO", "scope": "complete ordered pure SPE; not a half-coverage or mixed-security counterexample", "security": {"value": "9", "primary": ["13/45", "11/45", "2/9", "11/45", "0", "0"], "dual": [{"rivals": [0, 0, 5], "probability": "1"}]}, "expected": {"unit_customers": 61, "outcome": [0, 0, 0, 5], "utilities": ["9", "9", "9", "11"], "W": 38, "OPT": 61, "tau": "45/2"}}
STRATEGY NON-ACTION FIELDS: {}
root: 0
depth 1; for each lex prefix, digit j gives prescribed action at prefix+(j,)
root:000000
depth 2; for each lex prefix, digit j gives prescribed action at prefix+(j,)
0:000000 1:000000 2:000000 3:000000 4:000000 5:000000
depth 3; for each lex prefix, digit j gives prescribed action at prefix+(j,)
00:555554 01:500000 02:500000 03:500000 04:500000 05:400000 10:500000 11:000000 12:000000 13:000000 14:000000 15:000000 20:500000 21:000000 22:000000 23:000000 24:000000 25:000000 30:500000 31:000000 32:000000 33:000000 34:000000 35:000000 40:500000 41:000000 42:000000 43:000000 44:000000 45:000000 50:400000 51:000000 52:000000 53:000000 54:000000 55:000000
STRUCTURE ONLY: {"all_actions_unique": true, "exact_complete_history_keys": true, "all_labels_legal": true, "action_rows": 259}

# individual_security_failure
DATA: {"players": 3, "topics": ["X0", "X1", "X2", "Y0", "Y1", "Y2"], "customers": [{"topics": [2], "multiplicity": 1}, {"topics": [0, 1, 3, 4], "multiplicity": 4}, {"topics": [0, 2, 3, 4], "multiplicity": 3}, {"topics": [1, 2, 3, 4], "multiplicity": 3}, {"topics": [0, 1, 2, 3, 4], "multiplicity": 2}, {"topics": [5], "multiplicity": 1}, {"topics": [0, 1, 3, 5], "multiplicity": 3}, {"topics": [0, 2, 3, 5], "multiplicity": 3}, {"topics": [1, 2, 3, 5], "multiplicity": 3}, {"topics": [0, 1, 4, 5], "multiplicity": 3}, {"topics": [0, 2, 4, 5], "multiplicity": 3}, {"topics": [1, 2, 4, 5], "multiplicity": 3}, {"topics": [0, 1, 3, 4, 5], "multiplicity": 2}]}
UNIT CUSTOMER COUNT: 34
CERTIFICATE NON-ACTION FIELDS: {"security": {"primary": ["5/41", "5/41", "21/82", "5/41", "5/41", "21/82"], "dual": [{"rivals": [0, 1], "probability": "23/82"}, {"rivals": [0, 2], "probability": "9/82"}, {"rivals": [1, 2], "probability": "9/82"}, {"rivals": [3, 4], "probability": "23/82"}, {"rivals": [3, 5], "probability": "9/82"}, {"rivals": [4, 5], "probability": "9/82"}], "value": "2411/246"}, "scope": "Full-history individual mixed-security failure; not an aggregate BR or half-coverage counterexample."}
STRATEGY NON-ACTION FIELDS: {"terminal_counts": [1, 0, 0, 1, 1, 0]}
root: 0
depth 1; for each lex prefix, digit j gives prescribed action at prefix+(j,)
root:333000
depth 2; for each lex prefix, digit j gives prescribed action at prefix+(j,)
0:121433 1:200433 2:100433 3:100454 4:100533 5:100433
STRUCTURE ONLY: {"all_actions_unique": true, "exact_complete_history_keys": true, "all_labels_legal": true, "action_rows": 43}

# eight_cce_welfare_gap
DATA: {"topics": ["T0", "T1", "T2", "T3"], "customers": [{"topics": [0, 2, 3], "multiplicity": 2}, {"topics": [1], "multiplicity": 4}, {"topics": [2], "multiplicity": 1}, {"topics": [3], "multiplicity": 1}], "players": 3}
UNIT CUSTOMER COUNT: 8
CERTIFICATE NON-ACTION FIELDS: {"terminal_counts": [1, 2, 0, 0]}
STRATEGY NON-ACTION FIELDS: {"terminal_counts": [1, 2, 0, 0]}
root: 0
depth 1; for each lex prefix, digit j gives prescribed action at prefix+(j,)
root:1111
depth 2; for each lex prefix, digit j gives prescribed action at prefix+(j,)
0:1111 1:1232 2:1311 3:1211
STRUCTURE ONLY: {"all_actions_unique": true, "exact_complete_history_keys": true, "all_labels_legal": true, "action_rows": 21}

# coverage_opportunity_failure
DATA: {"topics": ["A", "B", "T", "D", "E"], "players": 3, "customers": [{"topics": [0], "multiplicity": 2}, {"topics": [1], "multiplicity": 2}, {"topics": [2], "multiplicity": 1}, {"topics": [2, 3], "multiplicity": 1}, {"topics": [2, 4], "multiplicity": 1}, {"topics": [0, 3, 4], "multiplicity": 3}, {"topics": [1, 3, 4], "multiplicity": 1}]}
UNIT CUSTOMER COUNT: 11
CERTIFICATE NON-ACTION FIELDS: {"terminal_counts": [2, 1, 0, 0, 0]}
STRATEGY NON-ACTION FIELDS: {"terminal_counts": [2, 1, 0, 0, 0]}
root: 0
depth 1; for each lex prefix, digit j gives prescribed action at prefix+(j,)
root:00000
depth 2; for each lex prefix, digit j gives prescribed action at prefix+(j,)
0:13343 1:30000 2:30000 3:40000 4:30000
STRUCTURE ONLY: {"all_actions_unique": true, "exact_complete_history_keys": true, "all_labels_legal": true, "action_rows": 31}

# prefix_balance_failure
DATA: {"topics": ["L0", "A", "B", "L1", "L2", "L3"], "customers": [{"topics": [0], "multiplicity": 2}, {"topics": [0, 1], "multiplicity": 1}, {"topics": [0, 2], "multiplicity": 2}, {"topics": [3], "multiplicity": 2}, {"topics": [1, 3], "multiplicity": 1}, {"topics": [2, 3], "multiplicity": 2}, {"topics": [4], "multiplicity": 2}, {"topics": [1, 4], "multiplicity": 1}, {"topics": [2, 4], "multiplicity": 2}, {"topics": [5], "multiplicity": 2}, {"topics": [2, 5], "multiplicity": 2}, {"topics": [1, 2, 5], "multiplicity": 3}], "players": 4}
UNIT CUSTOMER COUNT: 22
CERTIFICATE NON-ACTION FIELDS: {"terminal_counts": [0, 1, 3, 0, 0, 0]}
STRATEGY NON-ACTION FIELDS: {"terminal_counts": [0, 1, 3, 0, 0, 0]}
root: 1
depth 1; for each lex prefix, digit j gives prescribed action at prefix+(j,)
root:221222
depth 2; for each lex prefix, digit j gives prescribed action at prefix+(j,)
0:222222 1:222222 2:221222 3:222222 4:222222 5:222222
depth 3; for each lex prefix, digit j gives prescribed action at prefix+(j,)
00:222222 01:222222 02:223222 03:222222 04:222222 05:222222 10:222222 11:222222 12:222222 13:222222 14:222222 15:222222 20:223222 21:222222 22:321001 23:220222 24:220222 25:221222 30:222222 31:222222 32:220222 33:222222 34:222222 35:222222 40:222222 41:222222 42:220222 43:222222 44:222222 45:222222 50:222222 51:222222 52:221222 53:222222 54:222222 55:222222
STRUCTURE ONLY: {"all_actions_unique": true, "exact_complete_history_keys": true, "all_labels_legal": true, "action_rows": 259}

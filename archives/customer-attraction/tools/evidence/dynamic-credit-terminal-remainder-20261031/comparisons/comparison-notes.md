# Dynamic-credit terminal remainder audit comparison

- source ID: `df15c429ac7f43dd83a8`
- source path: `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/background_probe/audit_terminal_profit_remainder.py`
- source SHA-256: `09c206124cfe699d1ee3f9368274be934a441ba499e991851f1e9baed6f9766c`
- source size: 2589 B

The script was read and run once. It performs 4394 exact Fraction local identity checks over b,e,d in 0..12 and l in {0,1}; it then checks a 69-customer scalar example with actual=(0,0,0,5), comparison=(0,1,2,3), P=48, v=18, comparison profit=69, L=51/2, K=15/2, J=0 and total remainder 33. The output explicitly says the universal proof is in a companion note and finite checks do not prove generality; `full_SPE_reaudited=false`.

Compared with the archived `任意背景的末位利润精确余项分解--引理`, this is an implementation audit of its local identity and scalar record, not a new derivation. It preserves the distinction between a末位 exact remainder and the unresolved early-credit/payment bridge.

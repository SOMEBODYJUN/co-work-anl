# 可信回复与末位响应者审计原件

数学合同与证据关系见[正式计算对象](../../../state/计算/可信回复与末位响应者的精确审计--计算.md)。

| 原件 | 源ID | 字节数 | SHA-256 |
| --- | --- | ---: | --- |
| [audit_terminal_responder_exchange.py](audit_terminal_responder_exchange.py) | b55d3b1e2ae7035fede7 | 2070 | 8a7e446a00445c6c6cc77fa906d42496d1251e548aba0c37016400ae8818bccf |
| [audit_terminal_responder_exchange.json](audit_terminal_responder_exchange.json) | d15f77e2b8f0dd330d78 | 9934 | 01509e15f9a628ef85e8bafe72e96e89b297b08a128a4dba5685bcfa32b002e7 |
| [audit_response_defect.py](audit_response_defect.py) | cda57043c0e6fb35c448 | 3387 | b9ed614e63b2240e150916cc62713b0a4d8eff0f836e22a0580f03a8edb91285 |
| [audit_response_defect.json](audit_response_defect.json) | 51686270adf809c5b7c9 | 273715 | 2e1635c342b4675c49feff031aa5bc4c6be012823c81134f31070f7620e434e6 |

四文件的旧目录均为 `research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/credible/`，在 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 分别有同字节定位。原 JSON 没有记录当年运行环境。此次实跑使用 Python 3.12.14，未改写原报告。

在本目录下运行下列命令。原脚本默认写同名 JSON 且拒绝覆盖，使用空临时目录，保留 Python 断言。

```sh
set -eu
replay_dir=$(mktemp -d)
cp audit_terminal_responder_exchange.py audit_response_defect.py "$replay_dir/"
python3 "$replay_dir/audit_terminal_responder_exchange.py"
python3 "$replay_dir/audit_response_defect.py"
cmp audit_terminal_responder_exchange.json "$replay_dir/audit_terminal_responder_exchange.json"
cmp audit_response_defect.json "$replay_dir/audit_response_defect.json"
python3 verify_reports.py
```

两个 `cmp` 均通过。原程序摘要依次为16条会员行与100个系数，以及128条身份式行、19个有限实例、首个超限 $k=7$。独立程序另核3078条指定查询和这些分支末位的143982个目录动作收益（含指定动作）。它通过读取冻结报告并重算客户负载验证，不导入原脚本，也不改变报告。末位检查以相应真实查询的前缀为条件；全部历史的可信性仍依据解析的完整SPE粘合。

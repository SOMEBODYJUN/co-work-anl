# 固定策略锥三种逐人接口的原始证据

四份原文按原文件名逐字节保留于original/，来源commit/path、稳定源ID、SHA256及尺寸见source-manifest.json。范围是round4_independent的README、probe_floors.py、cone_probe_results.json和candidate_near_kplus_0_kplus_3.json。数学说明见[正式程序对象](../../../state/程序/固定完整策略锥的三种逐人覆盖桥攻击--程序.md)。

原程序依赖源树tests/audits/customer_attraction_strategy_lp.py、两个旧证书及new_policy_security_cones.json.gz；迁移的original/probe_floors.py保留原相对路径，不能从这里直接调用并声称完整候选发现复现。保存候选near_kplus_0不在其冻结main列出的两命名来源或九锥报告中。

本次运行 `python3 archives/customer-attraction/tools/evidence/individual-floor-three-interface-original/verify_saved_candidate.py`，不导入原solver、LP或旧审计器，从保存127项重数及2801个完整历史动作重算19607个比较，并比较全部16807有序终局覆盖。结果在new-definition-replay.json。运行退出0；这只复核此有限证书，未执行原候选发生器、未重解九锥LP。

此前R-10559的independent_kplus_blind_checker.py及报告已对同SHA候选作过独立定义级审计，本次结果与其一致。来源独有增量、候选状态和后续纠错由正式正文分开说明。

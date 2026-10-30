# 实际执行与证据合同

9个原件逐份`work.py clean show ID --out path`实际取回，并按冻结inventory核SHA/size；source-manifest.json给原定位。未使用Git、claim、done、checkpoint或外发动作。

原程序复制到replay/facility_spe，原test复制到replay/tests；pure.py是本次旁取原1243字节依赖，bounded_overlap.py/mitm.py复用既有已整理原bytes，指纹见replay-manifest.json。没有改源。真实运行在仓库外cache/heterogeneous-code-examples-staging进行，环境PYTHONPATH指向该replay；execution JSON保绝对真实运行路径。

1. 原suite：`python3 replay/tests/test_heterogeneous.py --report replay/test-heterogeneous-report.json --example-out replay/first-long-cycle.json`，exit0，7.36秒；stdout/stderr及命令/exit/hash均保。
2. 新窄检查：`python3 -O audit_examples.py --output replay/examples-audit.json`，exit0；stdout/stderr、脚本、输入原bytes和完整逐格闭支持谱均保。五fixture、4族参数、六损坏、七元数据任意字符串、verify禁用make_menu、全默认规则为真实执行范围。不是第二份通用上界证明。
3. 原generator：`python3 replay/facility_spe/examples/tight_two.py --M 1000 --output replay/generated-M1000.json`，exit0。生成数据与两个原JSON相同；展示decimal不是证明。
4. asset-checks.json核9原hash和18889字节、两M1000唯一换行差、suite首长环JSON与six_cycle相等。

初始尝试恰遇Boss的done/sync临时暂存未跟踪原件，copy报FileNotFoundError，shell随后找不到suite入口，exit2。此时没有运行数学测试。Boss确认local_sync=synced、原件恢复后改在外置staging实际执行上述成功步骤。初始错误仅保原因及工具记录，不声称留有该次完整stderr，也不把它算作数学失败或成功测试。

一般因子二仍候选。verify对显式见证的直接检查、完整策略的规定默认规则、实例最优求解、独立开发、外审及文献优先权各自分开。

# 本次真实执行与离线复现

17主源canonical claim已pushed af7ef2d2f89ca712aa2c94c9991987bf0da09b38；本文数学交付仍是external本地草稿，未pushed/done。

本次4原入口只执行一次：threshold_dp.py原main、mitm.py --self-test、hardness_enum.py原main、bounded_overlap.py用author-example-input.json。run_originals.py保存实际cwd/命令/时间/stdout/stderr哈希。全部标准库、PYTHONDONTWRITEBYTECODE=1，无网络、无Git、无其他owner程序。原bounded示例源于原note明示JSON，helper没有修改原程序。

一次额外check_bounded_contract.py在python -O下运行：已有单混合区间/四单位极小回归和达到证书不调用枚举器、4种损坏证书显式拒绝。它是窄新核验，不是原历史300/100套件。

若有理由复现，先把本证据目录复制到临时路径，再运行 `python3 run_originals.py`；这会重写副本replay输出。补核可执行 `python3 -O check_bounded_contract.py`，其输入是副本replay/bounded-author-example.stdout.txt。当前成功无需重跑；MITM elapsed_seconds自然变化，数学计数与保存旧报告仅该字段不同。

本批没有运行五站/同址/稀疏/强弦/三次的新程序，亦未重复先前通过的多设施审计。所有28原件来源、完整commit/path、hash分别在provenance和related-provenance。旧外文/未附附件的未核范围见数学计算正文及delivery。

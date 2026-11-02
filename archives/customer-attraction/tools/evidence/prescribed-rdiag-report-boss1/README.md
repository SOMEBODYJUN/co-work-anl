# Rdiag指定路径六层原报告的冻结复放

本目录为既有程序对象“指定实际路径的全续局阈值审计”的有限输入运行证据，不是新的福利定理。原5199B报告已完整保存在 ../diagonal-seed-materialization-boss3/related/seed18_Rdiag_actual_prefix_audit.json，无需重复复制。

从仓库根运行：

```bash
python3 archives/customer-attraction/tools/evidence/prescribed-rdiag-report-boss1/replay.py
```

wrapper在仓库外时，可加一个位置参数指定仓库根。需Python、NumPy和SciPy；不联网、不读取凭据。它先从cleanup/inventory.jsonl核原报告、入口、两依赖及输入的size/SHA，然后在本证据目录内建会自动清理的临时布局，复制现有正式源，按原相对输入调用未改原audit入口。会覆写本目录verification.json、regenerated-report.json、stdout.txt和stderr.txt；冻结原件不改。

成功事件实际在Boss1隔离固定布局执行一次，exit0、stderr空，10.74秒；除seconds外整个报告字段和数组精确相同。后续原工作区sync暂移导致一次wrapper启动前找不到文件，没有第二次BI。发布wrapper只调整临时布局/仓库定位，ast解析通过，未为包装调整重复BI。因此本目录保存的verification.json对应真实成功事件argv/cwd，不能倒称最终包装入口的实测日志。

三个代码及输入均复用既有正式路径：menu-price-and-prescribed-prefix-audits-primary/frozen-inputs中的9536369246be24174433入口；bigint-interval-bi-and-controller-cone-primary/source-root原布局中的bigint_controller_attack.py与full18_cone_attack.py；diagonal-seed-materialization-boss3/original/seed18_Rdiag.json。完整冻结commit/path/SHA在verification.json。

全集递推按计数缓存同构子博弈的全部可实现SPE终局，保留任意有序历史和平局，非一张计数策略。原实现复放补齐此前只作标量核验的前四层阈值和retention。另有直接Fraction类型循环重算六实际/见证收益、差值和W；该循环不独立认证min/max与SPE成员资格。没有第二BI实现、完整有序策略证书、控制器锥、LP、随机发现或一般六人断言。

# R-18 next_security 有限搜索

冻结源：`cc26f08fdbca875077fa`（README）、`40e27b1e71a331c1bde9`（abstract_alternating.py）、`fe59345cc04044139168`（300 seeds 结果）、`0575fb6aa8bc09ca066b`（background_search.py）、`2ab21fcd2cb6416a0ac9`（best JSON）。

本地复跑：

- `abstract_alternating.py --n 3 --topics 3 --seeds 300 --steps 6`：`candidate=null`，约 4.34 秒。
- `background_search.py --seed 201 --iterations 300 --topics 5 --remaining 3 --background 2`：best ratio=1.0，iteration 8，(P=34.7,v=11.566666...\)，未出现 `<1`。

这些都是浮点/LP 有限搜索。README 的高背景区间 (B\ge r-4) 条件不覆盖根空背景；Q-CAG-HALF 仍 OPEN。

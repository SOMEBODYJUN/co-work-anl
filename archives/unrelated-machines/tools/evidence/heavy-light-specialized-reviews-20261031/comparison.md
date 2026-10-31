# Heavy/light 专门审查源去重说明

本目录的两个稳定源已由 Boss2 用 `clean show` 全文实读：

- `3d13dfe877f2d2e2d5fa` 是重轻 saddle 证书的独立核对，保留可选 heavy 覆盖改变残余轻基线时的 `mu_j(lambda)` 差项、saddle 充分条件和二循环反例；
- `770f10f3898d0f4cb50b` 是大边匹配残余过滤/共享逃逸的独立重构，保留安全删边、simple-support/escape 参数族、有限穷举边界及“局部匹配不等于全局共享容量”的障碍。

两源的完整数学对象已经分别由 `archives/unrelated-machines/state/审查/重边匹配过滤与重轻对偶循环双源审查--审查.md` 与 `archives/unrelated-machines/state/审查/重型匹配凸化与逃逸残余审计--审查.md` 承接；本批没有新的量词、算法或反例对象。因此处置为 duplicate，保留原全文副本、SHA manifest 和这份比较说明，不把同一 heavy/light 主题重复登记。

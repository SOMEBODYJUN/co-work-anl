# 背景旧覆盖付款系数证书搜索程序

主源 b634158696869226b89c 已完整正常 clean show 并核2041B原字节，保存于[original/fresh_cover_cost_certificate.py](original/fresh_cover_cost_certificate.py)。[正式程序对象](../../../state/程序/背景旧覆盖付款的系数证书搜索程序--程序.md)自足解释任意合法有序背景、同一SPE真实回复、24列192行、额外tau付款条件、成功分支验收、默认失败与tau1正面条件证书。

[source-manifest.json](source-manifest.json)给双冻结提交、blob、SHA及依赖；[related/R5bb00-README.md](related/R5bb00-README.md)只作工作区原路线比较，不新增primary处置。[comparison-manifest.json](comparison-manifest.json)保全仓比较后的七正式对象指纹和区别。

唯一原运行由[run_original.py](run_original.py)复制未修改源码到新目录完成。它无tau参数覆盖，恰执行默认tau2一次；[replay/execution.json](replay/execution.json)记录0.904312249秒、exit0、1次192×24 LP、stderr空、源码前后SHA同。原成功分支没有执行，不能声称原有理余项断言通过。

[新报告](replay/fresh_cover_cost_2.json)与[stdout](replay/stdout.txt)各148B，SHA390eed8d1f1755881dc5afff4d20e3c275ec9313950897450a44c72e5766755b，完全同冻结失败报告；[stderr](replay/stderr.txt)为空。[运行范围](execution-scope.json)明确没有其他tau原入口、SPE搜索或全策略重跑。

配套[数据对象](../../../state/计算/背景旧覆盖二倍付款模板的不可行报告--计算.md)及[独立审计](../fresh-cover-cost-certificate-data/exact-audit.json)从单位份额核192×24系数，给八支持y、24非负配对及目标−6；同一见证适用于tau≥17/12，但未认证最优阈值。tau1四项有理证书另给40零/152正。该数据方唯一审计未调用原helper/main/LP，程序包没有重复它；[共享绑定](shared-audit-binding.json)保原文件指纹。

从仓库根复现到一个不存在的新目录：

```sh
python3 archives/customer-attraction/tools/evidence/fresh-cover-cost-certificate-program/run_original.py --source archives/customer-attraction/tools/evidence/fresh-cover-cost-certificate-program/original/fresh_cover_cost_certificate.py --out-dir /tmp/fresh-cover-cost-new-replay
```

命令是复现入口，不表示本轮又运行一次。wrapper核固定失败报告原字节；换求解器若输出不同文本会被拒绝作“原字节复现”，应单独记录。精确不可行性由有理Farkas证明承担，非浮点报错文本。

[check_package.py](check_package.py)只核SHA、共享证据、JSON/Python语法、链接和回执目标，不执行原源或数学审计；[artifact-manifest.json](artifact-manifest.json)与[self-check.json](self-check.json)保存交付绑定和静态结果。该条件模板失败不能否定全部两人背景界，既有52例根仍满足half，亦未给六人反例。

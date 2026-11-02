# 菜单实际价格源复核

正文：[目录价格与实际价格分离源复核](../../../state/审查/目录价格与实际价格分离源复核--审查.md)。

`verify_price_separation.py` 只检查一个冻结必要条件点的六条实际价格与一个共同容量。它核两份小原件及完整点的字节身份，调用未修改的冻结原审计CLI一次，再独立按hist汇总菜单一阶矩后重算全部价。`verification.json` 是本次成功输出，包含16个hist的末价贡献；没有调用母矩阵builder、优化器或SPE求解器。

从仓库根运行：

```sh
python3 archives/customer-attraction/subarchives/six-providers/tools/evidence/boss6-menu-actual-prices/verify_price_separation.py --repo "$PWD" --out archives/customer-attraction/subarchives/six-providers/tools/evidence/boss6-menu-actual-prices/verification.json
```

原输入复用已有正式证据，完整路径、SHA、双冻结提交和源ID见 `source-manifest.json`。脚本显式检查所有依赖的SHA，未复制或修改原件。当前输出只认证记载的价格算术，不认证5259个母行、共同目录实现或完整纯SPE。

# 局部势排除完整证书来源包

12份已认领源通过新版 `python3 work.py clean show ID --out ...` 逐份导出。原字节按 attack/potential_tax 与 review 的相对目录保存；`source-manifest.json` 给源ID、完整冻结提交/路径、保存地址、字节和SHA-256。两个冻结提交同字节，原件只保存一份。全部394888字节与clean show给出的指纹一致。

正式正文为[三人反例与六人实际嵌入](../../../state/反例/局部势排除损失的三人反例与六人实际嵌入--反例.md)及[完整策略程序合同](../../../state/程序/势排除完整策略的重构与双重核验合同--程序.md)。前者给全部621客户、31动作与155条IC证书、六人9331动作包及FFF实际背景的势分解；后者完整解释12源作用、外部依赖、输入绑定和各实现独立性的准确范围。

原三人逐单位报告绑定 `esm_exact_obstruction.json`；两份原六人报告均绑定 `six_esm_embedding.json`，三个绑定本轮均核对。原报告分别给155和55986项精确弱IC全部非负。本轮读完源码/报告，消费全部JSON字段与完整动作/所存IC记录，复用这些成熟报告，没有重跑全树效用计算、发现MILP、规范求解器或随机探索。`source-structure-inspection.json` 保存本轮结构核验及四行F静态势分解；这个PASS是结构/绑定检查，不能读成新一次全树精确审计。

`audit_esm_obstruction.py` 要读取未在本12源取得的发现JSON，执行有理化后生成三人包；原稿另称的 `verify_exact_obstruction.py` 未在本12源取得，不能冒名替换。`embed_six.py` 依赖原仓库的 customer_attraction 模块和原路径层级，是构造器。保存原程序不表示本目录具有从MILP到全树策略的全部发现依赖。两个逐单位核验器及作者六人核验器仅需标准库和已保存输入；它们会覆盖写报告，重放应先复制到临时目录并保持 attack/review 相对路径。

既有 [optimal-kernel-and-exclusion-source-primary](../optimal-kernel-and-exclusion-source-primary/README.md) 已保父方审查，BELL/TEL、r≤2和数值范围准确。本批补的是原完整策略/IC及程序身份，不将旧准确正文改成“本轮新独审”。单步ESM的FALSE不反总预算、成对候选或half；无最小性、外审或新颖性声明。

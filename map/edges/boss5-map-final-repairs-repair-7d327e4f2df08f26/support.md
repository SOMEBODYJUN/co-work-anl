# 737 dual/primal repair support

本 repair 完整复核十个 declared reference 与三个旧资产的 SHA。737 exact relaxation 保持：76 个正有理原子、737 条聚合行全部非负、W=1、O=beta=913780818510707039481129588377221884004224809337659/447470471154075773671105653556364606136051881479274≈2.042103060239853；57 个 full-type dual 权的最小 scaled residual 为 0，negative columns 为空，覆盖 47574 个 type contexts。这个结论只针对 737 必要信息松弛，不给真实五人 SPE 或 OPT_5。

binary64 的 1141 列不是精确 737 点：W−1=−22055/147573952589676412928，且 AB→AE:2O 与 AE→Sbranch:1O 两条新单行总和严格为负。该快照只作有限发现/实现轨迹。

现有 728↔737 交叉材料的两个精确分离仍成立：737 的 76 点违反 728 独有 jointfinal:AB:Sbranch:2O+3O，负值为

-34835181401157636064926624409276654055302863422723/447470471154075773671105653556364606136051881479274；

728 的 65 点违反 737 独有 crossfinal:AE:AB:2O，负值为

-11184644019172119707794458826327155614707/55747094649329780987868402069850796098656。

旧 canonical 文件把“互不包含”误写成单一 `implies/unconditional` 边；本 repair 不伪造新的 728 endpoint 读取，因此将其记录为待 owner 重绑的 context 比较。三条已有 HQR `checks/context` 边的方向和范围保持有效。旧 receipt 的 isolated/pending wording 由本 repair 取代。

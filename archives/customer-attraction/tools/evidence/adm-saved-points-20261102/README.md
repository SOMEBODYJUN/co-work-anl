# ADM两保存点与第四轮根稿六来源

Boss4 / cleaner，2026-11-02。本目录及两篇新正文目前仅本地保存，未确认pushed，未提交done。逐源候选记录在`cleanup/workspaces/Boss4/resume-20261102-boundary/PROPOSED_RECEIPTS.json`，必须先发布本文和全部依赖、核推送树，再逐源done。

六个primary原件共20,887B，均用当前`cleanup.show`读取冻结版本、核inventory SHA后保在`original/<完整源ID>/原文件名`。manifest保两冻结定位和全部字节指纹。五份正式比较材料从固定结果提交`8a5a74b032e330f43cbdd9da3c46495e511ffaed`读取，保在comparison；已按该提交tree中的Git blob逐份核同，不拿当前漂移URL作证。一次Git批量promisor取blob报bad revision，随后这些公开比较文本由固定commit原始URL取得，blob比对仍成功，没有重试认证。

## 数学入口

- [ADM程序合同及两有限精确证书](../../../state/程序/ADM探针的完整终局菜单与两保存点精确证书--程序.md)：完整m槽ADM并集、旧筛选/浮点发现范围，新Fraction原始/对偶夹证。
- [删当前SC与完整端点cap根接口](../../../state/资源/删当前自洽池与完整端点cap回收的根稿接口--资源.md)：四份根文的存在性、付款、反例、cap回收、提升和历史边界。
- [source-manifest.json](source-manifest.json)：六来源和五比较快照。
- [exact_saved_points.json](exact_saved_points.json)：全部十行菜单及两个有限问题的精确双边证书。
- [execution-notes.json](execution-notes.json)：实际执行次数与失败修正；未运行原发现器main、原四次发现或浮点LP。

复现最终有限核：

```sh
python3 archives/customer-attraction/tools/evidence/adm-saved-points-20261102/verify_adm_saved_points.py
```

输入`adm_discovery.json`与冻结d624353ed020110fb523逐字节一致，程序先检查其SHA，输出同时绑定checker自身SHA。只用Python标准库。第一例V=47/24<W/3=8/3；第二例V=53/17<W/2=9/2。两保存路径均可被完整SPE支持，根终局计数各8、完整cap菜单各10。递推允许全部弱平局、重复动作；按计数缓存依续局同构和独立有序子树粘接，非要求原策略匿名化。

新完整checker共两次入口：首版第一例对偶提取失败；诊断脚本另调用两记录，第一仍失败、第二成功；补齐零概率查询也可能紧的对偶约束后，最终两例一次完整入口exit0。没有用第一次空报告冒PASS，最终报告来自修正版成功入口；全部精确不等式已在报告中可独立代入。这些是知情新重构，不是原审计或盲审。

没有用两有限负gap证明一般ADM。四根源的纯点/全p反例没有解决六人half；保根银行矩阵与删当前、跨实际位置平均的非线性SC不是同一命题。关系证据仅先存Boss4工作区，第三阶段需保这些前提再建边。

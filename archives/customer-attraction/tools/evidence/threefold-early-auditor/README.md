# 三重早期覆盖含交集审计器：原入口复跑

正文：[三重早期覆盖的含交集系数审计器](../../../state/程序/三重早期覆盖的含交集系数审计器--程序.md)。主清洗源仅`82711e93237a7f66a20c`，其他来源是必要依赖/比较，不在本回执代领done。

## 原件与依赖

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `original/audit_threefold.py` | 3409 | `0b336908e52a26d5785ef048a9d80c6f79e0bad59f9c4bbf40d4f8c681da8b7e` |
| `original/research_1/threefold_penultimate_exact.json` | 1847 | `7adcce9a18beb2654c5fe1a4ef5dc45d8d130e8426f81928243cedd6ea75d35a` |
| `related/audit_threefold.json` | 1861 | `6b3ff9871170e1179e8d3df35c5e042788d33791541f82e803804faa88889783` |
| `related/threefold_penultimate_half.md` | 5181 | `6b1ec8fb4d89613f325beaf292a7cb078da8a03095e08d65a66148a45ccc63da` |
| `related/review_threefold.md` | 3176 | `90bd865e11853d794c62c1e6a49b0b69d82d9c7e22a663ae8ed8eb112f7e7d7b` |

以上均通过`clean show`取得冻结真实字节并全文阅读；完整来源ID/blob/提交见`source_manifest.json`。程序实际依赖的文件按`__file__`相邻目录定位，不由cwd或网络取得；依赖并不缺失。

## 实际重放

在仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/threefold-early-auditor/replay_original.py
```

本轮新增包装器将原脚本和真实相邻输入原样复制到`rerun/isolated/`，核验字节后在该隔离目录以独立未优化Python进程执行原`__main__`，捕获输出。它没有导入作者/父方系数函数进行替代，也没有改动原程序。原程序自身只打印JSON；包装器保存为`rerun/audit_threefold.json`，标准错误为`rerun/stderr.txt`。

Python3.12.14实际退出码0；stdout为1861B，与冻结报告字节完全相同，stderr为0B。运行前后源码与输入SHA不变。完整事实在`rerun/run_report.json`。脚本断言承担认证，重放明确禁用优化标志并去掉`PYTHONOPTIMIZE`；不能将关闭断言所得的`passed`视为有效复跑。

## 检查含义

原代码枚举64个实际六位会员型、49个比较/回复计数对及84个完整含交集计数三元组；全域3136投影型/5376含交集型中逐项核h消去。只对P3允许的42个实际型要求余项非负，因此受限计数为2058/3528，最小值0。

这些是完整客户系数域，不是游戏、SPE、客户数或目录数的有限搜索。逐客户P3半覆盖的全称结论还使用正文重建的真实S/Z/V/H/L非负行及求和。全域64型的rho可以为负，程序保留完整有符号表；本复跑没有证明它们总和对所有SPE非负。

原程序只读取作者输入中的`rho_actual_membership`和`complete_restricted_state_count`来做等值核对，其余作者字段未被程序检查。正文明确列出这个输入合同。另一个清洗Solver本轮独立五端点重建rho，见[报告对象](../../../state/计算/三重早期覆盖的完整残差有限表--计算.md)；这与本目录运行原实现是不同证据。

## 阅读与关系

除上表五项外，全文比较共同目录完整历史模型、真实末两人菜单交集消去、三重早期覆盖证书的含交集重构范围、倒二主题少量早期遗漏平方阈值。全仓搜索定位三重条件、三行与报告字段，未因旧审查曾写通过就跳过代码及真实依赖。

现行旧审查明确过去没有执行该代码；本页补本轮运行事实，不改过去身份。独有保留是程序的全部断言、h可行域/消去、P3与全域signed余项、相邻输入定位、只读取两字段的合同，以及断言必须启用。无P2/Farkas、无一般六人half、无外审或新颖性认证。关系解释写入正文，第三阶段再登记超边。

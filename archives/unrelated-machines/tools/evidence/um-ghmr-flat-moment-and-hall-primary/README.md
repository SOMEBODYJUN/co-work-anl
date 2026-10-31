# 五主源原实现及精确数据证据

本证据包对应Boss4正式认领合批20中的五份程序主源；其余15份不属于本包primary。实际claim为pushed/Boss4/synced，tip `372a7d401e044cd87f4457e55b6ae7e79704565a`；原始完整回执与分工子集分别保存在[claim-receipt.json](claim-receipt.json)和[assigned-subset.json](assigned-subset.json)。本包处于外部独立stage，写入结果仓库、checkpoint/push/done由Root串行办理；包本身不声称已推送或done。

## 自足数学与主实现

四份资源正文保存完整定义、证明承重、真实算法、有限域、边界和接续用途；已吸收的一般主定理不在本次重新授予。
- [GHMR任务权匹配的独立查询与共享逃逸检查--资源.md](../../../state/资源/GHMR任务权匹配的独立查询与共享逃逸检查--资源.md)
- [共同矩有理Gram平坦原子与低阶Latin点原入口--资源.md](../../../state/资源/共同矩有理Gram平坦原子与低阶Latin点原入口--资源.md)
- [半单位共同选择与同资格计数调度双入口--资源.md](../../../state/资源/半单位共同选择与同资格计数调度双入口--资源.md)
- [Hall共同宏组接收流的原实现与九矩阵证书--资源.md](../../../state/资源/Hall共同宏组接收流的原实现与九矩阵证书--资源.md)

## 五份逐主源原件

下列全部原文件在正式认领后完整读取，大小与SHA按冻结inventory核验；不是把早前comparison登记改称主源完成。

| ID | 路径 | 字节/行 | SHA-256 |
|---|---|---:|---|
| 013b8b02e1a84be3ae87 | [tests/audits/unrelated_machines/ghmr_independent.py](original/tests/audits/unrelated_machines/ghmr_independent.py) | 14986/359 | `ae062bb6bae27f996c4010fc5962aaee792e7e5030c34e833263089250d3e5ab` |
| e3f0fcf717accc012b76 | [tests/audits/unrelated_machines/global_assignment_flat_moment_audit.py](original/tests/audits/unrelated_machines/global_assignment_flat_moment_audit.py) | 16133/312 | `1dfcaee91aaa6886dae201f5b796decbab9e2b667bb96ff24285a6a00c118666` |
| 691288fa3b5382ea2d1d | [tests/audits/unrelated_machines/half_unit_joint_choice.py](original/tests/audits/unrelated_machines/half_unit_joint_choice.py) | 10910/258 | `2dce254733810a5dacaeeb4ef2c6d642584a3dbe9536a50966b14e99ea65f793` |
| 6daf56cc77a03b8dfe96 | [tests/audits/unrelated_machines/half_unit_schedule_independent.py](original/tests/audits/unrelated_machines/half_unit_schedule_independent.py) | 4469/115 | `7687957bc85bf9193ffb65ed2683365a3c054d52e1516392ede61c9377ac8506` |
| 9fa5bc2e0157bd3693a9 | [tests/audits/unrelated_machines/hall_group_joint_flow.py](original/tests/audits/unrelated_machines/hall_group_joint_flow.py) | 24011/510 | `ebcf08cbc82b841b86ab5c567d1abad79de0cf4b501bcffc24172fba3b94e46e` |

## 依赖、完整相关正文和冻结报告

15项均保原字节、来源blob/commit和实际阅读范围，详见[comparison-inventory.json](comparison-inventory.json)。518401B half JSON的头部/范围/历史身份实读，362个输入和逐delta结果及计数完整逐行独立语义核对；不把人工复述每个JSON字节作为核验方法。Hall九原矩阵、九证书和全部job身份无省略。

| ID/角色 | 原路径 | 字节 | SHA-256 |
|---|---|---:|---|
| 2dd3413231d9b1499f4c / runtime-dependency | [tests/audits/unrelated_machines/heavy_matching_residual.py](original/tests/audits/unrelated_machines/heavy_matching_residual.py) | 14747 | `63f64a5497223e451374c74359dade6bec14ea507b3ed901d8f9495a699f2deb` |
| b13ff01a2215f76cad57 / comparison | [evidence/runs/unrelated_machines/heavy_matching_residual_audit.json](comparison/evidence/runs/unrelated_machines/heavy_matching_residual_audit.json) | 9849 | `7ec7968f54cff7bc46452cbcadbf6969e968eab1af970e7c6abed256bbde591a` |
| 564cb5698086b3a591e3 / comparison | [evidence/runs/unrelated_machines/half_unit_joint_choice_audit.json](comparison/evidence/runs/unrelated_machines/half_unit_joint_choice_audit.json) | 518401 | `2bf32f90bcef806fa5a7e83efcf601be4b1e8abb1b7354bf08575dea1fd098aa` |
| 6b44adbc694f4eb1778f / comparison | [evidence/runs/unrelated_machines/hall_group_joint_flow_audit.json](comparison/evidence/runs/unrelated_machines/hall_group_joint_flow_audit.json) | 3455 | `3a4136a952a4b3adc0a833ab58d050eeb8d4ee2bcd21597fa7716e81fc6e6327` |
| 50558e252eca7ba30f02 / comparison | [examples/unrelated_machines/hall_group_joint_flow_cases.json](comparison/examples/unrelated_machines/hall_group_joint_flow_cases.json) | 11538 | `169e3e2e5c7d07828587df471f7c422ce95631b597fbce9a4e8263795c542322` |
| 40c22343bbac6390a1da / comparison | [evidence/certificates/unrelated_machines/hall_group_joint_flow_witness.json](comparison/evidence/certificates/unrelated_machines/hall_group_joint_flow_witness.json) | 7335 | `5dd49579e562044b5031b34a83f8d43af0bf527d0fa73f3516f43a34041f7208` |
| 43aee4f76d83e01522ad / comparison | [research/current/unrelated_machines/global_assignment_moment_rounding.md](comparison/research/current/unrelated_machines/global_assignment_moment_rounding.md) | 17973 | `c49e7d8dd13757f16ce6bd451c32999966739bed9be5c40d0bade4fce63cb1f0` |
| 0db3d973e7d68bc734c1 / comparison | [research/reviews/unrelated_machines/global_assignment_moment_rounding_review.md](comparison/research/reviews/unrelated_machines/global_assignment_moment_rounding_review.md) | 9154 | `854bcc711cf9aa9b60625aff8524db96ee831ac6c9355e2056b00da16a17aee5` |
| 483f65ab900b2bf9f8bf / comparison | [research/current/unrelated_machines/heavy_matching_residual_and_escape.md](comparison/research/current/unrelated_machines/heavy_matching_residual_and_escape.md) | 13978 | `3a4541eca4b8edbe02a37c3558f934e092d27a175c4ed6786c66dbeebb2422df` |
| 326d6af1da65fbe4ab4c / comparison | [research/current/unrelated_machines/hall_group_joint_flow.md](comparison/research/current/unrelated_machines/hall_group_joint_flow.md) | 11876 | `10aabd8e9cc0eccf10974f94e23633f6d1034313348a69ceac003bb876af5b2b` |
| 389c9eda10e6ce9f39a4 / comparison | [research/reviews/unrelated_machines/hall_group_joint_flow_review.md](comparison/research/reviews/unrelated_machines/hall_group_joint_flow_review.md) | 8846 | `7ddf4f1b7c4bfcd5003178e30723709bd00d4a00c11d5d9a999903f2544e96b8` |
| d45e652e9a9c66c8d850 / comparison | [research/reviews/unrelated_machines/half_unit_joint_choice_review.md](comparison/research/reviews/unrelated_machines/half_unit_joint_choice_review.md) | 9260 | `0fde78af36825a048869c700b83db12e5b96bcdd6c95867bfebad418d629aaab` |
| abbd6a205df15b9dce26 / comparison | [evidence/certificates/unrelated_machines/global_assignment_moment_freeze.json](comparison/evidence/certificates/unrelated_machines/global_assignment_moment_freeze.json) | 4786 | `8f4983cd7d7a4a890f0f5eca18723ef0a07960feb8af8c5503e3cebbbb678d81` |
| 1d8914155d1a253adfa9 / comparison | [research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md](comparison/research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md) | 17800 | `8cf637c20618062a98d4038e7873987acf06bf426a583a6a678d974d7b103ba3` |
| f9d501935cc79ff43f03 / comparison | [evidence/runs/unrelated_machines/heavy_matching_escape_independent.json](comparison/evidence/runs/unrelated_machines/heavy_matching_escape_independent.json) | 3040 | `7d8fda39f3b96028b14c1e68e104520ccc3dc600e2b07180091a077386a0e01f` |

## 实际执行和旧运行复用

**原程序新执行恰一次**：global_assignment_flat_moment_audit.py的完整main在事先不存在的新空目录运行，Python3.12.14，退出0，实际耗时0.30709531599859474秒。代码SHA为1dfcaee91aaa6886dae201f5b796decbab9e2b667bb96ff24285a6a00c118666，完整JSON输出SHA为6bd209971cc7ebe241263e6022054b04b706c5fee04f54efe35bc5b383c6c498。实际命令、cwd、输出事先不存在标志及运行事件见[execution.json](runs/global-flat-original/execution.json)，并保[完整报告](runs/global-flat-original/full-report.json)、[stdout](runs/global-flat-original/stdout)和[stderr](runs/global-flat-original/stderr)。旧freeze虽登记helper代码SHA，其canonical_path_reruns只列near-flat/独立HS/full-HS，不能据依赖导入虚报完整helper main已运行。

原main实际输入全内置于源码。[global-flat-built-in-inputs.json](inputs/global-flat-built-in-inputs.json)是四law全部原job/原子与Latin16三元组的文档化展开，**不是**CLI额外读取的输入文件。程序没有库外依赖，精确Fraction算术，无浮点/SDP。

其余四原程序新main运行均为0，准确复用以下同SHA完整旧报告：GHMR用f9d501…同时绑定独立脚本及被测依赖；两half程序共用564cb…绑定两代码SHA；Hall用6b44…绑定ebcf…当前代码，并用50558…/40c223…九矩阵证书核实际输入输出。旧报告若无退出码/耗时，则本包不补造。GHMR的被测依赖ownmain报告b13ff…单独比较，不重跑、不混进本主源28672/13824域。

## 新独立数据核对

[verify_saved_data.py](verify_saved_data.py)不导入任何原程序。最终版已执行通过，真实代码SHA/命令/cwd/exit0/耗时/stdout/stderr和输出SHA见[最终数据检查事件](runs/data-check-final/execution.json)及[data-selfcheck.json](data-selfcheck.json)。这是有限保存数据核对，不是额外原算法main或独立无界证明。自查开发中早一版本亦通过；交付只将最终源码与最终真实执行事件逐SHA绑定，不为早一版本捏造源码快照或耗时。

- GHMR独立反算28672匹配查询、13824合法矩阵、16000次T1可行调度出现，核三个展开/六压缩点与依赖61公式行；不重新调用原过滤器。
- half遍历全部362输入，直接求源3DM真值/首次matching，重建1448 delta查询结果及全部totals；另核独立265输入180YES。六份[完整原矩阵和σ](inputs/half-unit-six-full-matrices-and-witnesses.json)由本批反向构造或全small给出，明确不是旧程序JSON曾保存σ；两代码machine置换与时间倍数也列在文件。
- Hall逐九原输入重建所有job-major端，穷举共2152份合法完整assignment核九OPT，全部7成功证书的46job逐件核资格、真实时间和所有负载；[九例分配计数](saved-hall-nine-oracle-counts.json)保边界。这里不是重跑14798域原main。
- flat全部211矩重构、恢复两原子与四组feature秩独立核对，26原子共106个原job检查。Latin4用[16个精确字符值](inputs/latin4-exact-character-PSD-check.json)证低阶协方差PSD秩6，并检查1820个四组无perfect3DM；没有degree4调度局部化器，不称gap2。

## 版本、旧页澄清与关系

[comparison-findings.json](comparison-findings.json)记录所有量词/版本/运行身份差异；[relationship-review.json](relationship-review.json)解释四新对象与已存证明/审查的实现、有限检查及域差异联系。此为第二阶段关系判断，未直接改第三阶段超图。

旧共享页仅作原字节快照，三项[未应用建议](unapplied-formal-clarifications.json)逐条保存目标、精确旧SHA/原段/行号、建议替文和实际原代码或冻结字段依据：

1. Hall2773输出完全来自4448基础循环，所有2278真实T1可行均成功；多出的495为T1不可行但rhoT输出合法的基础输入，命名fixture/其他域未计入。
2. 组下界一般为(1/2+1/q)T；原Wh≥T反例是q2特例。
3. promise瓶颈B使用macro/home/receiver共同网络，不能只求macro/home匹配。

未覆盖、改写或重勾这些旧Boss2来源。四新资源均自足保更正后的准确数学。旧一般证明、内部独立检查、历史审者先验、外审、新颖性和一般UM目标保持各自状态。

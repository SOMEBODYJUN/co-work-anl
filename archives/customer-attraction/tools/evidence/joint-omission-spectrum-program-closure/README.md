# 联合前缀遗漏谱程序与双版报告

正式[计算对象](../../../state/计算/联合前缀遗漏谱的有限审计与双版报告--计算.md)说明全部数学范围、原程序、两个报告版本及证据局限。

三主来源原字节15010B，清单source-manifest.json给完整冻结来源、大小、SHA256和Git blob。原审计按原相对路径在source-root保留；四份必要规范包依赖由已有同SHA证据复用，见dependency-manifest.json。本批只对三主来源记语义处置，不对依赖代done。

原入口只打印JSON，程序本身不写任何报告。一次原入口运行退出0、stderr为空，stdout作为current-v2-report.json保存，与冻结v2逐字节相同。version-comparison.json还核旧首版为v2删去matching_obstruction_v2后的逐字节精确投影；这不等于运行了缺失的旧版代码。run-metadata.json保本次执行范围及环境。

30输入的全部174条可实现有序路径用于谱断言，只为每输入首条路径构造并核验一份完整证书，共30份；不是所有完整策略枚举。m13/20及匹配m5/13障碍只作客户类型压缩算术、谱和末位完整菜单，不求这些非SPE路径的均衡证书，不进行大人数SPE求解。

复用时保持source-root层次，运行其中research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/omission/audit_joint_omission_spectrum.py，把stdout重定向到新的结果路径即可。无第三方包、LP/MIP或外部输入要求。不要将有限重放、解析全分数行证书及任意人数定理混为一项认证。

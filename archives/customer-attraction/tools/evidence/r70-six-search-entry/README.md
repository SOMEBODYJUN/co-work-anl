# 六人随机输入入口的原件和单试次

正式对象为[六人浮点终局搜索的随机输入入口](../../../state/程序/六人浮点终局搜索的随机输入入口--程序.md)。主源1800B/SHA8c284c503fea834ac59b1529a791c1919740394ad9350e471cdf51459aa8055a，完整原件在original；实际6396B spe_dp依赖在related/six_1。原字节不改，完整接口精度和元数据比较由各源正文分别承担。

`run_one_original.py <全新clone外目录>`物化两个文件，唯一运行原seed981773/count1/topics7配置，经runpy+只读profile捕获sample/solve返回。一次约0.321秒，两源码前后SHA一致；main/sample/solve各1，LP/reconstruct/exact verify均0，未重跑默认1000。replay保存真实原stdout/stderr/new_best、只读capture及execution。

`audit_saved_trial.py`是新小整数覆盖核：98单位客户，返回计数覆盖95，枚举七个六标签支持的精确OPT6为98；没有DP/SPE/LP调用。其结论不认证该计数是SPE或最差SPE。原浮点比值近似95/98，不能把JSON多位小数称有理证书。

source-manifest保存主源和依赖版本、实际事件及输出指纹。原README/SIX_BRIEF/workspace由独立研究入口资源处置；这里不把历史研究合同当已经完成的数学证明，也不据此运行或迁移旧身份。

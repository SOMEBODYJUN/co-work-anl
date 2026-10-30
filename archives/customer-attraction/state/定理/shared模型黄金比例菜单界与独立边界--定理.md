---
id: "shared-model/golden-ratio-menu-boundary"
kind: "theorem"
type_tag: "定理"
title: "shared模型黄金比例菜单界与独立边界"
status: "conditional-frozen-certificates"
truth_status: "exact-certificates-in-independent-shared-model"
review_level: "full-source-read-no-transfer-to-CAG"
scope: "archives/certificates/shared中的设施/菜单模型；不属于CAG共同目录客户吸引模型"
summary: "两组five_site报告给出factor=3/2与809/500的25个连续分支精确证书；on_path_chord与tiny_phi给出黄金比例phi=(1+sqrt(5))/2的局部菜单保证。所有结论保留shared模型身份，不迁移到CAG half。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/five_site_a3_2_yes.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/five_site_a809_500_yes.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/on_path_chord.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/tiny_phi.json"
---
# shared模型黄金比例菜单界与独立边界

## 模型身份

这七份来源位于 shared 证书目录，使用设施布局、shared customers、共同客户概率和 guarded continuation 的语言。它们不采用CAG的共同有限集合目录、顺序提供者客户收益或六人半覆盖量词；因此所有结论必须保持独立模型身份，不能作为CAG定理或反例。

## 精确冻结证书

five_site_a3_2_yes 的 on_path layout 为 (0,3)，factor=3/2，保存25个 layout continuation，每个 continuation给出 shared索引、首设施概率和两侧loads。five_site_a809_500_yes 保留完全同一分支结构，factor=809/500，loads为大整数有理值；它不是浮点近似，源JSON直接保存整数。

on_path_chord 的 guarantee 是 phi=(1+sqrt(5))/2、factor=1。on_path layout (0,1) 有三个共同客户，首设施概率各39/80，loads为277/4与279/4；四条 deviation witness 都是 guarded_pure，response_cycle=(0,1,2)，9个ordered pair、33个menu entry。tiny_phi 同样给出黄金比例保证和factor=1，on_path为(4,3)，response_cycle=(4,3)，25个ordered pair、49个menu entry，并含两条two_designated_mixers witness。

这些是各自冻结JSON中的精确证书字段。它们证明所声明的局部菜单/布局保证在该shared模型实例上成立；不证明所有shared实例，更不改变CAG的开放状态。

## 用途和限制

可复用内容是“共同客户概率、guarded repair、响应环和菜单威胁”的证书表达，以及比较 factor 的精确有理接口。若第三阶段研究设施或菜单模型，应从原JSON重建布局和概率；若研究CAG，最多把它们作为外部模型启发，不能把phi、3/2或809/500当CAG支付行。原CAG目标、六人模型和证书量词均独立保留。

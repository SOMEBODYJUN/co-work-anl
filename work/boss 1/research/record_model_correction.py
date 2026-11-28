"""Record the audit correction without replacing the frozen original experiment."""
from pathlib import Path
from datetime import datetime, timezone
import json

R = Path(__file__).resolve().parent
W = R.parent
old = json.loads((W/'compute/outputs/historical-warning-v1-cdc109f9a414.json').read_text())['result']
new = json.loads((W/'compute/outputs/historical-warning-audit-v2-de6d97643789.json').read_text())['result']
audit = json.loads((R/'tasks/research_independent_review/independent_models.json').read_text())
rows=[]
for version, value in [('原实验，保留',old),('审计纠错重估',new)]:
    rows.append(f"| {version} | 常数基线 | {value['baseline']['brier']:.6f} | 0.5000 | 0/13 | 0/148 |")
    for name,v in value['models'].items():
        for mode,label in [('raw_test','raw'),('calibrated_test','校准')]:
            m=v[mode]
            false=round(m['false_alarm_fraction_negative_periods']*148)
            rows.append(f"| {version} | {name} {label} | {m['brier']:.6f} | {m['roc_auc']:.4f} | {m['detected_episodes']}/13 | {false}/148 |")
text='''# 历史预警：真实数据错误、修复与审计重估

独立执行者 `/root/research_independent_review` 从原始JST R6重新生成标签，发现爱尔兰1870—1919年的50个crisisJST缺值，其中35行进入原训练面板被误记为0。原脚本只从等于1的年份列事件，误将未知作为无危机。另有3行六个宏观特征全部缺失。两项错误都只影响训练段，但会改变拟合和后续校准。

boss 1修复 `tools/prepare_jst_example.py`：要求信息当年及未来三年危机指示均为观测的0/1；排除全特征缺失；部分特征缺失仍仅以训练数据拟合插补器。新面板1703行，训练1188、校准223、测试187；所有切分时间、特征、模型、阈值预算保持原定义。35+3行排除清单与脚本SHA在 `models/jst_audited_20261127/data_manifest.json`。原面板1741行、原输入、原结果均原样保留。

真实统一入口重估作业为 `historical-warning-audit-v2`，输入计划 `models/compute-audited-history.json`，输出 `compute/outputs/historical-warning-audit-v2-de6d97643789.json`。执行位置是本地9CPU，不是Codespace。

| 版本 | 方法 | Brier（低为好） | AUC | 检出事件 | 非事件年份误报 |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(rows)+'''

校准反转不是正负类别列取错。独立审计重建两类分类顺序均为[0,1]，逐预测与冻结输出差异不超过1.11e−16；旧HGB校准段原始AUC约0.4357，校准logit斜率−0.196335，独立二项似然优化也得到−0.196308。纠错后校准段原始AUC约0.4128、斜率−0.262958，仍反向。校准223国年仅覆盖9次事件，全球/国家相关性进一步限制可迁移性；这解释了链条如何翻转，不将小样本当作已识别的唯一原因。

用途裁决：拒绝本轮HGB校准链作主预警；logit仅作历史比较；所有模型拒绝用于中国事件概率。raw HGB在已见测试表现较好必须披露，但不能据此事后选择raw、重新调参再宣称独立验证通过。本次是有完整追踪的审计纠错重估，不是新的未见测试，不增加独立证据数量。

历史专题 `tasks/history_framework_review/history.md` 中3/13与0/13指旧实验校准后结果，冻结文稿保留当时版本；当前裁决和正式报告采用本纠错记录，并同时披露原结果。所有事件计数按预测窗内至少一次报警计，不是独立危机概率；187国年也不是187个独立事件。
'''
(R/'historical_model_correction.md').write_text(text)
record=json.loads((R/'data/method_review_revision.json').read_text())
record.update(published_at=datetime.now(timezone.utc).isoformat(),impact_note='独立审计发现未知标签被当负例，原实验保留；新作业纠错并定位校准负斜率，需更新模型用途节点。',text='实际已完成11个compute作业。旧JST输入1741行含35未知危机标签及3全特征缺失；修复后的1703行训练1188/校准223/测试187。纠错后logit校准Brier0.170316,AUC0.602737,检出3漏10,误报7/148；HGB raw Brier0.156506,AUC0.730596,检出7漏6,误报18/148；HGB校准Brier0.185399,AUC0.269404,检出1漏12,误报43/148；基准Brier0.175914。独立重估确认类别[0,1]无错列，校准斜率负，旧-0.196335/新-0.262958。保持原切分与参数，已见测试只作审计纠错不得称新验证，拒绝校准HGB主用途及全部中国概率。中国桥接同版MAE0.64347对基线0.34545。银行资本另作披露CET1桥接。详情historical_model_correction.md和compute账本。')
(R/'data/method_audit_revision.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('saved correction and MT001 revision input')

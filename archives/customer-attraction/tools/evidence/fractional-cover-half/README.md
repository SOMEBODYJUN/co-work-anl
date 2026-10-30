# 六人分数覆盖半覆盖证据

数学结论见[条件半覆盖定理](../../../state/定理/六人分数覆盖条件半覆盖--定理.md)，旧全客户端点见[端点推论](../../../state/推论/真实末两人全客户分数价格端点--推论.md)，执行范围见[计算资源](../../../state/计算/六人分数覆盖半覆盖的精确系数证书--计算.md)。

`original/`保存五份已认领冻结源的原字节，`manifest.json`记录源ID、完整commit及SHA-256。两主要冻结提交中的对应内容相同。

`replay/`保存原标准库程序两个模式的本轮输出，以及独立审计、哈希和JSON一致性摘要。原程序写报告到脚本旁边，因此应复制后执行，避免覆盖冻结文件：

```sh
python3 - <<'PY'
from pathlib import Path
import shutil
p = Path('archives/customer-attraction/tools/evidence/fractional-cover-half')
shutil.copyfile(p/'original/replay_fractional_cover_pair_half.py',
                p/'replay/replay_fractional_cover_pair_half.py')
PY
python3 archives/customer-attraction/tools/evidence/fractional-cover-half/replay/replay_fractional_cover_pair_half.py
python3 archives/customer-attraction/tools/evidence/fractional-cover-half/replay/replay_fractional_cover_pair_half.py --endpoint
python3 archives/customer-attraction/tools/evidence/fractional-cover-half/audit_coefficients.py
```

重跑后的重复脚本可删除；原版本已保存在`original/`。`audit_coefficients.py`仅用标准库Fraction，独立按正文行语义及有理乘子核全部128+128型、80个R投影矩形角点和160个strongPAIR原IC恒等式，并与冻结报告核对。它不导入原回放、LP或游戏求解器，不检查完整SPE策略树。一般行非负性由正文解析证明承担。

9/2模式残差最小0、9零型、最小正`123181/137388191`；21/5模式最小0、14零型、最小正`687259/75190400`。两个条件证书均不宣称无条件六人half、阈值锐性、外审或新颖性。

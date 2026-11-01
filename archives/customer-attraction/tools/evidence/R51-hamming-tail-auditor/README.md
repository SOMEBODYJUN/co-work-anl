# R51汉明尾部独立审计器

主源`0a373b467b7bf2d0be8b`通过正常`clean show`完整取得并实读，原3072字节源码保存为[原程序](original/audit_hamming_tail.py)，SHA-256 `d7f3b3fc99f4d58cad64d267459423b5ed366d70a050429a9fdeaa068a67cd02`。比较来源为[9758字节旧报告](original/hamming_tail_audit.json)和[4951字节原独审稿](original/hamming_tail_blind_review.md)，两份均全文读取；比较来源不由本程序回执代登记。

原程序只有标准库依赖和内置参数，无外部输入/项目导入/随机性/文件写入。assert开启原样执行一次，完整命令、Python、起止时间、退出码及哈希在[event.json](run/event.json)；[stdout](run/stdout.json)9758字节与旧报告逐字节相同，[stderr](run/stderr.txt)为空。可在本目录执行`python3 original/audit_hamming_tail.py`复现stdout；原程序不读取同目录JSON。

结果20组，近轨12205、尾层406555项含自身动作比较，未来A历史640；d=1的10组完整覆盖全部有序历史并认证给定策略为全效率纯SPE，d≥2另10组各核明确远轨负行，不能混称全SPE通过。源码运行不包含六人，也没有这20组中的half负例。原盲审的历史身份与本轮知情重放分开。

正式说明见[审查对象](../../../state/审查/R51汉明尾部审计器--审查.md)；来源、比较对象与全部本地文件指纹见[manifest](manifest.json)。已有主障碍证明、发现方8组计数/样本程序和后续区间剪枝全效率定理的范围分别保留，不相加运行数或倒填执行史。

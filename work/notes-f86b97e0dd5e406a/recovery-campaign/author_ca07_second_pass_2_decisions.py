#!/usr/bin/env python3
"""Write an explicit Boss draft; this does not edit the formal note plan."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'work/notes-f86b97e0dd5e406a/notes/CA07/project'
OUT = P / 'audit/second-pass-2-merge'


def main():
    plan = json.loads((P / 'content-plan.json').read_text())
    blocks = {b['id']: b for k in ('transcription_blocks', 'study_blocks') for b in plan[k]}
    edits = {}

    def bid(short):
        return ('CA07-TRANSCRIPTION-' if short[0] == 'T' else 'CA07-STUDY-') + short[1:]

    def sid(page, unit):
        return f'CA07-P{page:03d}-U{unit:02d}'

    def native(page, unit):
        return f'audit/source-units-800/{sid(page, unit)}-800.png'

    def edit(short, text=None, sources=(), paths=()):
        key = bid(short)
        entry = edits.setdefault(key, {'target_id': key,
            'before_text_sha256': hashlib.sha256(blocks[key]['text'].encode()).hexdigest(),
            'add_source_ids': [], 'evidence_paths': []})
        if text is not None:
            entry['text'] = text
        entry['add_source_ids'] = sorted(set(entry['add_source_ids']) | set(sources))
        entry['evidence_paths'] = sorted(set(entry['evidence_paths']) | set(paths))

    def text(short):
        return edits.get(bid(short), {}).get('text', blocks[bid(short)]['text'])

    def replace(short, old, new):
        before = text(short)
        assert before.count(old) == 1, (short, old)
        edit(short, before.replace(old, new))

    def paired(raw, study, new):
        old = text(raw)
        replace(study, old, new)
        edit(raw, new)

    paired('T013', 'S005', r'$\exists a_i\in A,\ n\ge1$ $b^n+a_1 b^{n-1}\cdots+a_n=0$〔首项后的加号按上下文排写，原短横与长斜笔之间有白缝。次项高位原有角折、细点和长弯，按降幂语境拟为 $n-1$。中隔为一条细上斜及远处较高针点，点旁有极淡尾；此处未见另一个加号，省略号只标省写位置。末项前的加号有交叉；末 $a$ 的低附有短鼻、圆肩和左下开口，按 $n$ 形保留，未闭的 $0$ 仍是字形候选。〕')
    edit('TV-003', r'''> [!info] 指标与省写恢复
>
> 首项后的两笔虽相离，结合多项式各项的连接按加号理解；中隔的细上斜和远高针点只显示省写位置，不能说原处还写了一个加号或三个等距点。次项上方的角折、细点和远处长弯按降幂语境恢复为 $n-1$。规范加和可写成 $b^n+a_1b^{n-1}+\cdots+a_n=0$，这里补全的项间运算属于说明层。
>
> 末系数下附略倾 $n$ 形，但左下开口也容许未闭的 $0$；它是常数项这一事实不能决定作者选用的指标名。正文保留其笔形限制，规范定义可另用 $a_0,\ldots,a_{n-1}$ 编号，不以重编号反推原字。''')
    replace('S006', r'原次项高位的角折、点与弯笔按系数序次恢复为 $n-1$，不视为清楚的独立数字。',
        r'原首项后的横、斜两笔相离，按加和语境恢复为加号。次项高位的角折、点与长弯按降幂语境恢复为 $n-1$；中隔只有细上斜和远高针点，没有另一个独立加号。原末系数低附略倾 $n$，左下开口仍容许未闭 $0$。它处于常数项并不能决定原指标名；上面的 $a_0,\ldots,a_{n-1}$ 是规范重编号，不把它反当原墨证据。')

    paired('T022', 'S011', r'$\forall m\ge n,$ $1,\ldots,b^{n-1}$ 是一组生成元〔$1$ 后有低逗，其右先见细上挑、再见较短粗斜；两墨彼此分离，$b$ 前未另见逗。省略号及其后的逗号是省写序列的排版。“是一组生成元”为上下文恢复：“是”收笔贴后字，其后有独立一横、左折右拱低回及长挑穿短笔；“成元”较清楚，整句不按每字清晰识读。〕')
    paired('T034', 'S016', r'$\varphi_b(a_i)=d_{i\,\text{〔离体短横〕}\,1}a_i+\cdots d_{ri}a_i$〔三个被作用或相乘元素都写 $a_i$；首系数的长下笔按 $1$ 恢复，其收笔没有下一行 $j$ 的大回钩，离体短横另存。已写加号之后是分开的细斜与较长浅波弯，排印省略号只表示这两墨所在的省写位置。〕')
    edit('T033', sources=[sid(3,3)], paths=[native(3,3)])
    edit('S007', sources=[sid(1,u) for u in range(22,26)] + [sid(4,8)],
        paths=[native(1,u) for u in range(22,26)] + [native(4,8)])

    paired('T056', 'S022', r'$(3)\Rightarrow(4)$ $A[b]\subseteq M,$ $M$ 有 $Ab$ 模，〔原 $Ab$ 没有独立方括。〕 $m\in M$，$a\text{〔左向形〕}A[b]$〔$a$ 右边的长横伸近 $A$，左端有上长斜和下短回；原形不直接排成完整的属于号。〕')
    scalar_note = r'第四页末 $a$ 右边的左向形按“从 $A[b]$ 取标量”理解，规范写作 $a\in A[b]$；第五页随后另有清楚的 $a\in A[b]$。把前一形视为压写的属于号也与数学语义相容，但不能由语义断定原笔就是完整的 $\in$，更不把它当作已经定义的环同态 $A[b]\to a$。'
    replace('TV-015', '> （4）回（1）使用忠实性。', '> ' + scalar_note + '\n>\n> （4）回（1）使用忠实性。')
    replace('S024', r'将 $a\in A[b]$ 对 $m\in C$ 的作用定义成 $am$。', scalar_note + r' 将 $a\in A[b]$ 对 $m\in C$ 的作用定义成 $am$。')

    paired('T064', 'S035', r'''$$
k[b]=\{f(b):f\in A[T]\}\qquad f(b)\cdot V=f(b)(v)
$$

〔$f(b)$ 后的分隔是右上细斜与左下圆点，冒号为集合语法的排印。$A[T]$ 的 $T$ 横穿主竖；右折括后另有一条近竖微弯，右花括按集合收尾排写，原未见清楚的花括腰。作用左端为大 $V$ 形，右括内为小 $v$ 形；等号右邻接的两个括号压写。〕''')
    paired('T065', 'S035', r'$V$ 是 $k$ 有限生成〔“限生”中间交叉、回弯密连，按上下文恢复；末“成”右近细点、远处另有短斜墨。〕， $V$ 有一个 $k[b]$ 模〔此处括中字左斜落入低处开口回弯，右端短上挑；$b$ 为上下文恢复。〕')
    paired('T066', 'S035', r'$V$ 是一个忠实 $k[b]$ 模〔此处括中字为更低的开口回弯，右侧回升较长；$b$ 为上下文恢复。左括顶横下另有独立针点。〕')
    replace('TV-017', r'本段高斜干接低圈的算子字按 $b$ 排写；这与把同一算子改名为 $\sigma$ 无关，不将其说成原笔清楚写了希腊字母。',
        r'算子引入处和集合定义处的高斜干接低圈按 $b$ 排写；后面两条模句的括中字各为开口回弯，$b$ 是上下文恢复。第六页商式中的同手 $b$ 也有开口回卷，说明开口本身不决定它是另一个字母。各位置仍保留各自原形，不把同一算子改名为 $\sigma$ 当作原笔已写希腊字母。')
    replace('S036', r'本段算子原字是高斜干接低圈，按 $b$ 排写；$\sigma$ 可作改名，但不是原笔已清楚分出的希腊字母。',
        r'算子引入处和集合定义处是高斜干接低圈，按 $b$ 排写。后面两条模句的括中字分别为较浅和较低的开口回弯，$b$ 属上下文恢复；第六页商式的同手 $b$ 也有开口回卷，故不能只据开口判作另一个字母。$\sigma$ 可作改名，但不是原笔已清楚分出的希腊字母。')
    for short in ('TV-017','S036'):
        edit(short, sources=[sid(6,3)], paths=[native(6,3)])
    replace('TV-017', '> 系数应取 $k[T]$，',
        r'> 集合中的冒号与右花括是按语法配齐的排印，原分隔两墨和末尾近竖已在黑字处分别说明。系数应取 $k[T]$，')
    replace('S036', r'原系数处写 $A[T]$，本例应为 $k[T]$。',
        r'原系数处写 $A[T]$，本例应为 $k[T]$；集合分隔的两墨及末尾近竖保留在黑字注中，冒号与右花括是语法配齐的排印。')
    image_warning = r'两条模句在此均解释为算子像代数 $k[b]$ 的作用。若将开口字另作形式变量 $U$ 而取全多项式环 $k[U]$，令 $U$ 作用为 $b$，则在有限维 $V$ 上评价有非零核：$V\ne0$ 时有限维算子空间使充分多的 $b$ 的幂线性相关，$V=0$ 时常数 $1$ 已零化全体。因此不能把像代数的忠实性直接赋给全形式多项式环；此检验支持语义恢复，并不独自锁定原字。'
    edit('TV-017', text('TV-017') + '\n>\n> ' + image_warning)
    edit('S036', text('S036') + '\n>\n> ' + image_warning)

    # Evidence is linked per changed claim; all three full reports will also
    # be retained as independent records in the frozen receipt.
    root6 = 'audit/boss-recovery-6/'
    target_evidence = {
        'T013':[native(1,25),root6+'p1-polynomial-middle-marks-1200.png',root6+'p1-polynomial-first-operator-1200.png',root6+'p1-polynomial-final-coefficient-1200.png'],
        'TV-003':[native(1,25),root6+'p1-polynomial-middle-marks-1200.png',root6+'p1-polynomial-first-operator-1200.png',root6+'p1-polynomial-final-coefficient-1200.png'],
        'T022':[native(2,14),root6+'p2-generator-middle-marks-1200.png'],
        'T034':[native(3,5),root6+'p3-expansion-middle-marks-1200.png'],
        'T056':[native(4,23),'proposals/ca07_math/second-pass-2/p4-U23-a-connection-1200.png'],
        'TV-015':[native(4,23),native(5,3)],
        'T064':[native(5,12),native(5,13),'proposals/ca07_math/second-pass-2/p5-U13-ending-stroke-1200.png'],
        'T065':[native(5,16),'proposals/ca07_math/second-pass-2/p5-U16-inner-letter-1200.png'],
        'T066':[native(5,17),'proposals/ca07_math/second-pass-2/p5-U17-inner-letter-1200.png'],
        'TV-017':[native(5,u) for u in (10,11,12,13,14,16,17)]+[native(6,3)],
    }
    for key, paths in target_evidence.items():
        edit(key, paths=paths)
    for source, target in [('T013','S005'),('TV-003','S006'),('T022','S011'),('T034','S016'),('T056','S022'),('TV-015','S024'),('T064','S035'),('T065','S035'),('T066','S035'),('TV-017','S036')]:
        edit(target, paths=target_evidence[source])

    labels = {
        sid(1,25):'整关系：首运算位横斜相离、次幂断形；中隔细上斜和远高针点，末项前实交叉加号，末系数低附n/未闭0样',
        sid(2,14):'1后低逗、细上挑与较短粗斜，b前未另见逗；高指数与整句草写生成元说明',
        sid(3,5):'φ_b展开三处a_i；首d下i、离横、上下文1；已写加号后细斜和浅波两墨，末d_ri',
        sid(4,23):'m∈M及a与A[b]间的左向形：长横近A，左端上斜和下短回',
        sid(5,12):'k[b]={f(b)；b高斜低圈，f(b)后的分隔为右上细斜与左下圆点',
        sid(5,13):'f∈A[T]；T横穿主竖，右折括后另有近竖微弯收笔',
        sid(5,16):'V有一个k[开口回弯]模；有后孤横和分开的折竖，括中字按上下文恢复b',
        sid(5,17):'V是一个忠实k[低开口回弯]模；括中字按上下文恢复b，左括顶横下独立针点',
    }
    reports = [f'proposals/ca07_{role}/second-pass-2/second-pass-report.{ext}'
               for role in ('visual','math','adversarial') for ext in ('json','md')]
    math_addendum = ['proposals/ca07_math/second-pass-2-edge-addendum/edge-check.json',
                     'proposals/ca07_math/second-pass-2-edge-addendum/edge-check.md']

    def proof(method, inputs, result):
        return {'status':'pass','method':method,'inputs':inputs,'result':result}

    def rec(number, correction, sources, paths, selected=None, candidates=(), forward=None, backward=None, observation=None, targets=()):
        value = {'recovery_id':f'CA07-R{number:03d}', 'correction':correction,
            'source_ids':sources,'evidence_paths':sorted(set(paths+reports)),
            'related_target_ids':[bid(t) for t in targets]}
        if selected is not None:
            value['selected_text']=selected
        if candidates:
            value['additional_candidates']=[{'id':f'boss-sp2-alt-{i+1}','text':c} for i,c in enumerate(candidates)]
        if forward:
            value['forward_validation']=forward
        if backward:
            value['backward_validation']=backward
        if observation:
            value['return_to_image']={'observation':observation}
        return value

    recoveries = [
        rec(8,
            '两稿删除次项后没有独立原墨支持的额外加号，逐处分记首运算位的相离横斜、中隔两墨、末项实加号及末指标n/未闭0的边界；蓝式才补规范加和。独立数学员关于首两笔相交的旧观察由其冻结勘误替代。',
            [sid(1,u) for u in (23,24,25)],
            [native(1,u) for u in (23,24,25)]+target_evidence['T013']+math_addendum+[root6+'readonly-R008-operator-and-index-1200.json'],
            selected='原首运算位横斜分离按加号拟读；次幂角折、点和长弯按n−1恢复；两墨省写前不再补黑字加号，末项实加号保留。末低附按n形保留并说明未闭0仍为字形候选，蓝定义可重编号。',
            candidates=['首运算位仅把短横当减号，长斜单留；中隔与末指标皆按原形保留。系数变号仍可首一，数学本身不能排除此符号形的比较。',
                        '中隔直接排完整+⋯+并把末低附定为0。此作规范表达可成立，但第三加号没有独立原墨，0也不能由常数项地位独断。'],
            forward=proof('定义前提和降幂序次的正向检验','U23的A系数、U24的n≥1、U25首项b^n及后续项位置',
                '按首一关系理解各项，次项n−1与后文降幂相容；首后两互补方向的笔和末前实加号支持拟+。这个语义恢复不声称各省项的加号或完整数字均写清。'),
            backward=proof('重复最高幂、系数改名与运算形的反向检验','次幂候选n、末指标候选0、首运算位候选减号样',
                '若次幂也是n，最高系数1+a_1未必首一。末指标改名0不改变常数项，首后换减号也可吸收入系数，二者的数学可行性都不能确定原墨；保留局部形貌和候读限制才忠实。'),
            observation='首后短横在长斜前停止，中有白缝。次项高位角折、细点、长弯之外，中隔是带较暗起点的细升斜及更右更高针点，点旁极淡尾，未见第三加号。末项前横竖相交，末a低附短鼻接圆肩、右回长弯、左下开口。',
            targets=('T013','TV-003','S005','S006')),
        rec(12,
            '在两稿生成元行就地记录1后低逗与其右两段分离中隔，说明b前的逗号属于列表排印；原整句草写限定和强归纳不变。',
            [sid(2,u) for u in (5,6,10,11,12,13,14)],
            target_evidence['T022']+[root6+'readonly-middle-mark-inventory.json'],
            selected='原1后低逗，再有细上挑和较短粗斜，两墨作省写位置；b前未另见逗，规范列表标点有局部说明。生成短句按整句语境恢复，蓝强归纳证明保持。',
            candidates=['将第二短粗斜判为b前逗，首细挑独作省略。它与前低逗的高低、走向不同，且距b仍远，故不作确定原逗。',
                        '只用标准三点并省略两笔形貌。虽能表达数学序列，却不能说明实际两组墨，不采为保真层。'],
            observation='1后有低斜逗，右边先一带粗起点、向上渐淡的细挑，再一段较短较粗向右下收的斜墨；它们彼此分开，b前大片留白。后面的整句生成元草语是另一处恢复。',
            targets=('T022','S011')),
        rec(17,
            'T033显式援引相邻标量线性式，补P003-U03的目标来源和逆向落点，并挂该原生图；线性选读、两候选及既有正反检验不变。',
            [sid(1,10),sid(3,3),sid(3,4)],
            [native(1,10),native(3,3),native(3,4),root6+'readonly-T033-mapping.json'],
            targets=('T033','S016')),
        rec(18,
            '在两稿系数展开同一行补明实加号后的细斜和浅波两墨；不与首d下离横或下一组式的点横混合。',
            [sid(2,22),sid(3,5),sid(3,6),sid(3,7)],
            target_evidence['T034']+[native(3,6),root6+'readonly-middle-mark-inventory.json'],
            selected='原三个a_i、首d下i/离横/上下文1及末d_ri继续保留；实加号后细斜和较长浅波是省写位置，排印省略号不声称已有三点或另一加号。蓝一般求和不反写原式。',
            candidates=['把右浅波判为另一加号。它没有独立配对竖笔，数学需要相加不能补作原墨。',
                        '把展开式中隔直接认作标准三点，或借下方U07的点横填此空。两处属于不同物理行，不能互借。'],
            observation='U05首d低位的i点竖、离横和长下笔与中隔分开。原交叉加号右有一条渐淡细斜，另一段较长浅波微有起伏，两段间白；之后末d和a_i另起。',
            targets=('T034','S016')),
        rec(34,
            '两稿集合定义的局部注补上分隔两墨和末尾近竖，将冒号/右花括明确为语法恢复；改正台账把本处T冠横称为离体的旧观察。A[T]原错和蓝k[T]仍分层。',
            [sid(5,u) for u in (10,11,12,13)],
            [native(5,u) for u in (10,11,12,13)]+target_evidence['T064']+[root6+'readonly-R034-R035-small-marks.json'],
            selected='原系数A[T]保留，T横实穿主竖；f(b)后右高细斜和左低圆点按冒号排印。T后右折括外另有独立近竖微弯，右花括是集合收尾恢复并就地标明。蓝用已给标量域k作评价。',
            candidates=['外末笔为极简右花括，继续排}但必须注其近竖、无清晰折腰。',
                        '仅保末近竖作独立笔，不直接赋花括；在蓝层配齐集合界。其所在位置及左开括支持收尾功能，不支持另设未定义对象。'],
            forward=proof('集合构形与算子评价的正向检验','U10有限维k空间，U11算子，U12左开集合及分隔，U13原A[T]',
                '用k标量乘恒等算子，令T送b，便有f(b)组成的像子代数。左开界、分隔和尾笔位置支持按集合语法配齐，但不改变实际笔形。'),
            backward=proof('未知系数作用与外闭笔的反向检验','假定任意A系数可直接评价，或末竖本身已有完整花括腰',
                '原未给A到算子环的结构，不能直接评价任意A系数；末笔只有近平滑竖弯，数学需闭集合不能证明纸上有标准花括腰。'),
            observation='U12分隔上件是偏右细斜并带浅尾，下件为偏左实圆。U13 A双斜交横；T冠横穿主干，其右先折括回收，再有独立长近竖、微向右鼓的末笔。',
            targets=('T064','TV-017','S035','S036')),
        rec(35,
            '两处模句分别注明括中字的浅开钩和低回杯及b为上下文恢复，U17括冠下独立针点另记。蓝注限制高斜低圈的适用位置，给P6同手开口b对照，严格区分像代数与形式多项式环的忠实性。',
            [sid(5,u) for u in (10,11,12,14,16,17,19)]+[sid(6,3)],
            [native(5,u) for u in (10,11,12,14,16,17,19)]+[native(6,3)]+target_evidence['T065']+target_evidence['T066']+[root6+'readonly-R035.json',root6+'readonly-R034-R035-small-marks.json'],
            selected='原作用左V右v和两个压括、一/个文字保留；两模句括中分别开口浅回和更低回卷，b依邻近定义作上下文恢复，左括孤针另记。蓝作用始终是像代数k[b]，不将未取商的k[U]自动判忠实。',
            candidates=['把两处当同手b的开口变形，保k[b]但逐处记原形；P6同手开口b支持可能性，不能机械地只按闭圈认b。',
                        '把两处保为u/开弯候形，语义仍由评价像恢复；若直接按全形式环k[U]且声称忠实则反例与有限维关系排除。'],
            forward=proof('算子像定义、同手字形与作用的正向检验','U12定义的像，U14算子求值，U16/U17的两条模句及U10/U11有限维算子前提',
                '像内S作用为S(v)，复合、恒等和分配给模公理；零化所有v的算子为零，像作用忠实。U12与P6U03对照容许开口b，仍需各自保形。'),
            backward=proof('形式环核与压括类型的反向检验','将开口字直接作形式变量U，或把原右压括强读成f(bv)',
                '有限维非零V上，有限维End_k(V)迫b的充分多幂相关，给k[U]评价的非零核；V=0则1在核内，所以形式环作用均非忠实。bv为向量非多项式的算子实参，不能只据压括强断f(bv)；这不证明原字唯一是b。'),
            observation='U16内字左斜较高、下接宽浅开钩、右端短挑。U17内字下探更深、右侧回升较长、上口未闭；其左括的离冠与下兜之间有针点。U12典型b高干低圈，P6U03同手b也可开口；U19低弯形式变量仅为比较，不能单凭开口混同环。',
            targets=('T065','T066','TV-017','S035','S036')),
        rec(51,
            'R051/I051补U22元素类型与U23系数所在环的直接来源和验证证据；T015/S006原边已齐。S007重新使用定义，另补U22–25及P4U08五条真实目标边，不以其他目标已有边替代。末b/A字形结论不变。',
            [sid(1,u) for u in (22,23,25,26)],
            [native(1,u) for u in (22,23,24,25,26)]+[native(4,8)]+math_addendum+[root6+'readonly-R051-premises.json',root6+'readonly-R051-premises-view-receipt.json'],
            targets=('T015','S006','S007')),
    ]
    new_recoveries = [{
        'recovery_id':'CA07-R058','issue_id':'CA07-I058',
        'source_ids':[sid(4,23),sid(5,1),sid(5,3)],
        'problem':'P4U23中a与A[b]之间的原符有左向形和接近A的长横；两稿旧版直接排标准属于号，须分别恢复原笔与后文标量类型。该疑点独立于同处Ab缺括及下一页做乘法的动词。',
        'candidates':[
            {'id':'shape-and-membership','text':'原层保a〔左向形〕A[b]并说明上长斜下短回、长横伸近A；蓝由下一页明确a∈A[b]和am作用恢复为取该环中标量。'},
            {'id':'compressed-membership','text':'把原符视为压写的∈，排所属号但必须就地说明宽下弧不全、长横伸近A的形貌。'},
            {'id':'selection-arrow','text':'把左向形读成从A[b]选a的方向记号；语义仍是成员条件，不据此另造环到单元素的同态。'}],
        'selected_candidate_id':'shape-and-membership',
        'forward_validation':proof('相邻作用与后文独立所属式的正向检验','P4U23的m∈M和a的关系；P5U03明写a∈A[b]；P5U01在C中做am',
            'a作为A[b]标量而m作为模元，取M=C且对该环稳定时乘积有定义；后文的清楚所属式确认对象类型，原左向笔形仍在黑层保存。'),
        'backward_validation':proof('元素/映射类型及近邻字形的反向检验','将左向形断为环同态A[b]→a，或称原∈的全部弧横已清楚写足',
            'a未被定义为目标环，也没有新函数，因此不能解释为已经引入的环同态。P5U03的所属外弧与内横分开，而本处左端不对称且横伸很长；数学取元语义容许连写∈或选取箭样，不能独自确定原笔为标准符。'),
        'observation':'P4U23中a后长横伸至A左斜附近，左端上长斜与下短回呈左向形；同单元前m的所属外弧较完整。P5U03再次写a∈A[b]，弧与内横分离，可独立作语义和同手对照。',
        'related_target_ids':[bid(t) for t in ('T056','TV-015','S022','S024')],
        'evidence_paths':sorted(set([native(4,23),native(5,1),native(5,3),
            'proposals/ca07_math/second-pass-2/p4-U23-a-connection-1200.png',
            'proposals/ca07_visual/second-pass-2/crops/p4-u23-membership-1200.png',
            root6+'readonly-R058-and-R034.json']+reports)),
    }]
    expected = {n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ('source-transcript.md','study-notes.md','source-target-map.json')}
    out = {'boss_id':'BossNotes-2ff3215d6446','note_id':'CA07',
        'status':'draft awaiting all three independent frozen records',
        'document_hashes_before':expected,'target_edits':list(edits.values()),
        'source_labels':[{'source_id':s,'label':label} for s,label in labels.items()],
        'recoveries':recoveries,'new_recoveries':new_recoveries,
        'source_observation_record':'proposals/ca07_visual/second-pass-2/reconciled-source-observations.json'}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'boss-decisions-draft.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'target_edits':len(edits),'source_labels':len(labels),'formal_content_edited':False}))


if __name__ == '__main__':
    main()

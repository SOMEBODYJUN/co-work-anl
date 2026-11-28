"""Build a transparent publication/event index; never treat row counts as independent evidence."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

W = Path(__file__).resolve().parents[1]
S = json.loads((W / 'research_state.json').read_text())['sources']


def publication_key(row):
    url = row.get('original_source_url') or row['url']
    p = urlsplit(url)
    # NBS repeats an unchanged article in several navigation sections.
    match = re.search(r't(\d{8})_(\d+)\.html?$', p.path)
    if p.netloc.endswith('stats.gov.cn') and match:
        return 'NBS-article-' + match[2]
    # The identical MOF article is reachable from app, department and main domains.
    if p.netloc.endswith('mof.gov.cn') and match:
        return 'MOF-article-' + match[2]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), p.query, ''))


manual_events = [
    ('NBS-GDP-2026Q3-release', ['E01', 'E02', 'MA007'], '同一GDP发布和其摘录，不增加独立证据。'),
    ('NBS-real-estate-2026M10', ['E08', 'E09', 'E10', 'E11', 'E12', 'PF009'], '同一地产发布的多个字段。'),
    ('NBS-price-70cities-2026M10', ['E44', 'PF010', 'PF038'], '数据表及官方解读为同一调查事件；解读是另一篇文章。'),
    ('MOF-fiscal-2026M10', ['E18', 'E19', 'E20', 'E21', 'PF018'], '同一财政发布的多个字段。'),
    ('PBC-finance-2026M10', ['E22', 'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'MA004'], '央行同月贷款、存款、社融与货币的联合发布家族；多家转载不作独立证实。不同表的边界仍保留。'),
    ('NBS-economy-2026M10', ['E29', 'E41', 'E42', 'MA002'], '同一经济运行发布。'),
    ('PKU-microbusiness-2026Q3', ['E38', 'E39', 'E40', 'MA008'], '同一支付宝活跃经营者问卷及其原机构摘要。'),
    ('NFRA-banking-2026Q3', ['E31', 'E32', 'E33', 'E34', 'BK001', 'BK002'], '同季监管发布：原网页摘要与分机构、指标附件，非三份独立样本。'),
    ('MOF-conference-20261023', ['PF026', 'MA011'], '同一发布会的不同议题摘录。'),
    ('Dingnan-budget-2026-report', ['PF035', 'PF036'], '同一县预算报告的不同附件；不能作为两个独立县。'),
    ('ICBC-2026-capital-issuance', ['BK014', 'BK009'], '同一资本发行方案的不同程序阶段；拟发行、审核、注册和到账不能合并成一个已完成事实。'),
]
pubs = {}
for sid, row in S.items():
    key = publication_key(row)
    group = pubs.setdefault(key, {'publication_key': key, 'evidence_ids': [], 'urls': [], 'reported_dates': [], 'families_as_recorded': []})
    group['evidence_ids'].append(sid)
    for field, value in [('urls', row['url']), ('reported_dates', row['published_at']), ('families_as_recorded', row['source_family'])]:
        if value not in group[field]:
            group[field].append(value)

events, assigned = [], set()
for event, ids, reason in manual_events:
    ids = [sid for sid in ids if sid in S]
    if not ids:
        continue
    assigned.update(ids)
    events.append({'event_id': event, 'evidence_ids': ids, 'rationale': reason})
for key, group in pubs.items():
    remaining = [sid for sid in group['evidence_ids'] if sid not in assigned]
    if remaining:
        events.append({'event_id': 'publication-' + hashlib.sha256(key.encode()).hexdigest()[:12], 'evidence_ids': remaining, 'rationale': '在未识别其他共同事件时按出版物归并；不声称经济或统计独立。'})

result = {
    'schema': 'cncrisis-curated-lineage.v1',
    'input_kind': 'real_research',
    'evidence_record_count': len(S),
    'publication_locator_group_count': len(pubs),
    'event_or_publication_group_count': len(events),
    'count_interpretation': '这些是索引组数，不是独立证据样本量，也没有用于加权或概率。相同官方表可同时支持多条边，但只采集一次。原source对象、未知原发日期和seed_status均不改写。',
    'publications': sorted(pubs.values(), key=lambda x: x['publication_key']),
    'events': events,
    'explicit_limitations': [
        '政府转载的央行原稿仍属PBC来源家族；转载发布日期不是央行首发时刻。',
        '作者文章引用同一官方数据不创造独立事实；观点比较另记推理与假设。',
        '同一银行季度和中期报为同一家银行连续观测；不能当四家银行或独立随机样本。',
        '跨年份的NBS/MOF原发布保留修订版本差别；同一统计体系仍有共同测量误差。',
        '本索引不覆盖任何未上传的个人Library文件。'
    ]
}
(W / 'research/source_lineage.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['evidence_record_count', 'publication_locator_group_count', 'event_or_publication_group_count']}, ensure_ascii=False))

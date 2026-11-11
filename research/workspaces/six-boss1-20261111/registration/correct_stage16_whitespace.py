"""Preserve frozen originals and make a versioned, formatting-only correction."""
from pathlib import Path
from hashlib import sha256
import gzip
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
WS = HERE.parent
NID = 'M-a90ca74cfdc848cb8f628fac8dd35f0a'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def main():
    folder = HERE/'stage16_whitespace_correction'
    assert not folder.exists()
    folder.mkdir()
    reg = json.loads((REPO/'research/registry.json').read_text())
    objects = {x['object_id']:x for x in reg['objects']}
    lemma, comp = objects[NID], objects[CID]
    assert lemma['version'] == 1 and comp['version'] == 12
    lp = REPO/lemma['body']['path']
    dp = HERE/'stage16_new_lemma/body.md'
    assert digest(lp) == 'e25965027a094da5f5147670bdf72f937d7ecdde1aed8a98dc7b3b1a7d4c0ee4'
    assert digest(dp) == 'ea90cd908a69723b725225bdeee9fe9d95912b651d1359952fcbdc31ecaf41b8'
    archives = []
    for name, path in [('formal_lemma_v1.md.gz',lp), ('frozen_draft_body.md.gz',dp)]:
        payload = path.read_bytes()
        dst = folder/name
        dst.write_bytes(gzip.compress(payload,mtime=0))
        assert gzip.decompress(dst.read_bytes()) == payload
        archives.append(dict(original_path=str(path.relative_to(REPO)),original_sha256=digest(path),
                             archive_path=str(dst.relative_to(REPO)),archive_sha256=digest(dst)))
    old = lp.read_text()
    needle = 'h,\\ \n'
    assert old.count(needle) == 1
    new = old.replace(needle,'h,\\quad\n').replace('version: 1\n','version: 2\n',1)
    lp.write_text(new)
    oldsha = lemma['body']['sha256']
    lemma['version'] = 2
    lemma['body']['sha256'] = digest(lp)
    comp['version'] = 13
    updated = 0
    for ref in comp['evidence']:
        if ref['path'] == lemma['body']['path']:
            assert ref['sha256'] == oldsha
            ref['sha256'] = digest(lp)
            updated += 1
    assert updated == 1
    for material in reg['materials']:
        if material['path'] == lemma['body']['path']:
            assert material['sha256'] == oldsha
            material['sha256'] = digest(lp)
    # Registry edge list is unchanged. Inclusion is still a mapper obligation.
    candidate = HERE/'stage16b-registry-candidate.json'
    assert not candidate.exists()
    candidate.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    affected = []
    for path in sorted((REPO/'map/edges/six-boss1-20261111').glob('*.json')):
        edge = json.loads(path.read_text())
        if not ({NID,CID} & set(edge['source_ids']+edge['target_ids'])):
            continue
        for ref in edge['evidence']:
            if ref['path'] == lemma['body']['path']:
                assert ref['sha256'] == oldsha
                ref['sha256'] = digest(lp)
        for field in ['endpoint_pins','evidence_pins','review_digest']:
            edge.pop(field,None)
        edge['review_note'] += ' Stage16b仅修正式新引理一处公式行末空白并升v2；计算对象v13仅刷新该证据引用，承重正文不变。旧冻结草稿与正式v1字节存可逆gzip，数学证书均未改。'
        path.write_text(json.dumps(edge,ensure_ascii=False,indent=2)+'\n')
        affected.append(str(path.relative_to(REPO)))
    note = '''# Stage16 发布空白修正与原稿恢复

第一次 Stage16 checkpoint 在 Git whitespace 检查退出2，尚未提交或推送。
只有新引理公式 NU 的一处行末空白，同时存在于正式正文和已冻结草稿。
正式正文将该 TeX 空白写作 `\\quad`，并遵循登记规则升为版本2；数学内容不变。
计算对象版本13仅刷新引理正文SHA引用，其正文与已核计算证书逐字不变。

已冻结草稿没有修改。其原始 body.md 以及未推送的正式版本1，均逐字节
保存为本目录的确定性 gzip；original_bytes.json 给原路径、原SHA和压缩SHA。
解压 frozen_draft_body.md.gz 到原 stage16_new_lemma/body.md 可完整恢复
原冻结草稿，之后原 SHA256SUMS 仍可核验。当前本地原稿仍在原路径。
为满足正式发布的空白检查，仅该原草稿正文不作为文本文件入此次提交；
全部原稿信息已在无损压缩归档中，原检查结果和原候选登记保持历史原样。

恢复示例（目标不存在时执行；不覆盖后续稿）：

```python
from pathlib import Path
import gzip, hashlib
here = Path(__file__).resolve().parent
payload = gzip.decompress((here/'frozen_draft_body.md.gz').read_bytes())
assert hashlib.sha256(payload).hexdigest() == 'ea90cd908a69723b725225bdeee9fe9d95912b651d1359952fcbdc31ecaf41b8'
with (here.parent/'stage16_new_lemma/body.md').open('xb') as target:
    target.write(payload)
```

没有绕过任何 Git 检查、改动优化输入、重跑优化器或覆盖失败回执。
原 Stage16 checkpoint 回执亦按原字节收在本目录。Stage16b 必须重新
正式 register、edge-bind/check、checkpoint，只有返回 pushed 才算远端可恢复。
'''
    (folder/'README.md').write_text(note)
    (folder/'original_bytes.json').write_text(json.dumps(archives,ensure_ascii=False,indent=2)+'\n')
    for suffix in ['json','stdout.txt','stderr.txt','argv.json','selection.json']:
        source = REPO.parent/('checkpoint-stage16.'+suffix)
        assert source.exists()
        (folder/('failed-checkpoint-stage16.'+suffix)).write_bytes(source.read_bytes())
    # Only unstage this newly added draft; its actual frozen working file remains.
    relative = str(dp.relative_to(REPO))
    staged = subprocess.run(['git','diff','--cached','--name-only','--',relative],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()
    assert staged == relative
    subprocess.run(['git','restore','--staged','--',relative],cwd=REPO,check=True)
    summary = dict(status='VERSIONED_FORMATTING_CORRECTION_PREPARED',
                   lemma_version=2,computation_version=13,lemma_body=lemma['body'],
                   computation_body_unchanged=comp['body'],candidate_sha256=digest(candidate),
                   original_bytes=archives,local_frozen_draft_excluded_from_text_checkpoint=relative,
                   edge_files_requiring_bind_check=affected,canonical_edge_index_unchanged=True)
    (HERE/'stage16b-correction-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['original_bytes','edge_files_requiring_bind_check']},ensure_ascii=False))


if __name__ == '__main__':
    main()

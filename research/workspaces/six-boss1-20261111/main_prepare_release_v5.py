"""Main's explicit final-source assembly release, after independent proof checks.

Authorizes construction only, never optimization or implicit source discovery.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json

W=Path(__file__).resolve().parent
R=W.parents[2]
P=W/'visible_maximum_joint_v5'
def h(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def order(rows):return sha256((json.dumps([r['name'] for r in rows],ensure_ascii=False,separators=(',',':'))+'\n').encode()).hexdigest()
def write(p,d):
    with p.open('x') as f:f.write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

specifications=[
 ('source2_minimal_cap_safe',28,'raw_rows',['exact_family','sha256'],['exact_family','raw_rows'],True,
  'main_minimal_cap_source2_check.json',
  'd63c117b0adf2353f70ffaf7d959dd91e8c4ee378838f7e5f4af6e99c86861ec',
  'dfdadf4dec0cc1b135cb015fc60ba92f2208a8678a02835003213faefdc3161f',
  'e0686cf9db0ab9611eea9852a2e56141e24d9011d124ec2a881a10c8dc5f48d6'),
 ('all_source_minimal_cap_safe',1096,'raw_rows',['exact_family_sha256'],['raw_rows'],False,
  'main_all_source_minimal_cap_safe_check.json',
  'cabb420531d2ca22c27f3dd3a415cbe350807f2ff377178d2cff239ba8a02c83',
  '1c1964d14006b8c471e4a5b431b156c00373da28da8e87f08a1b084d5b9c0855',
  '30e2f3add32ec4d49192325dbe706e9d1c7e958722df0402d4699991fd9f69b6'),
 ('ordered_minimal_cap',137,'raw_row_count',['files','exact_family.json'],['raw_rows'],False,
  'main_ordered_minimal_cap_check.json',
  'cd0b3db1fe384f5a4336edca3ec6c9e954ac253748cd830f2858add37e96cdd7',
  '813a720751f8468f27955602d1b25ac3a4ca79da8777384067ae6a735aac61fe',
  'db6dd7c970ff5a525ad8b86f23640025ec5f66b250eccc85ad48f522e9fe401d')]

def main():
    assert not (P/'final_release.json').exists()
    contract=read(P/'preparation_contract.json')
    release=read(P/'final_release.template.json')
    release['append_sources']=deepcopy(contract['known_append_sources'])
    checksum_counts={}
    for package,count,countkey,fampath,countpath,ceq,checkfile,msha,fsha,psha in specifications:
        src=W/package
        assert h(src/'freeze_manifest.json')==msha
        assert h(src/'exact_family.json')==fsha
        assert h(src/'proof.md')==psha
        check=read(W/checkfile)
        assert check['status'].startswith('PASS_MAIN_') and check['optimizer_calls']==0
        n=0
        for line in (src/'SHA256SUMS').read_text().splitlines():
            expected,name=line.split(None,1); name=name.strip()
            path=R/name if name.startswith(('research/','archives/')) else src/name
            assert h(path)==expected,(package,name)
            n+=1
        checksum_counts[package]=n
        fam=read(src/'exact_family.json');rows=fam['rows']
        assert len(rows)==count==fam[countkey]
        files={name:h(src/name) for name in ['exact_family.json','freeze_manifest.json','proof.md',
                'coordinate_contract.json','literal_checker_output.json']}
        for name in ['source_manifest.json','source_pins.json','family_source_manifest.json',
                     'parameter_families.json','parameter_domains.json','parameter_polytope.json']:
            if (src/name).is_file():files[name]=h(src/name)
        release['append_sources'].append({
            'package':package,'rows_key':'rows','count_key':countkey,'raw_count':count,'files':files,
            'manifest_family_sha_path':fampath,'manifest_raw_count_path':countpath,
            'row_order_sha256':order(rows),'row_order_policy':'literal_source_order',
            'first_row_name':rows[0]['name'],'last_row_name':rows[-1]['name'],
            'excluded_rows':[],'new_numerical_divisor':'25','terminal_BR_mean_weight':'1',
            'terminal_BR_weight_field':'terminal_BR_average_weight',
            'uses_C_equality_in_source':ceq,'additional_equality_elimination':False,
            'main_source_review_complete':True,'main_check_file':checkfile,'main_check_sha256':h(W/checkfile)})
    old=P/'source_review.md';saved=P/'stage1_source_review.md'
    with saved.open('xb') as f:f.write(old.read_bytes())
    old.write_text('''# FINAL_COMPLETE_SOURCE_REVIEW

Boss1/Main；RUN six-boss1-20261111。完整准入范围固定为3056原行：
1586旧全域行、181固定帽同菜单完整cell行、28固定基点联动帽行、
28自由最小帽C-only行、1096五源八目标一般行、137新五查询最小帽行。
全部来源已停止写并冻结；无支持/点筛选，零行、重复行、根行全部保留。
只准构造及字面检查，本文件不授权优化器。新lambda[9,16]族单独研究，不进入本输入。

Main已亲读两份新proof.md全文。源预算、真实内部SAFE、共同菜单索引条件、
根六个不可删除的双缺面、坐标最小帽、全连续域严格d=1比较均核对成立。
独立Main程序main_minimal_caps_complete_check.py不导入任何来源程序：分别重建
两套45面/137顶点，全部12026边界组合、每面准确秩；从真实尾份额重新求
16656与49968隐藏态及全部弱平局最小值；按这些最小值重建562248与70281系数。
ordered还检查完整13568菜单上下文。两份结果均PASS、0优化、未读候选点。
源2 C-only另由main_minimal_cap_source2_check.py全28域/3584态/14364列验证，
有符号C等式乘子允许−11/20，一般T的S和H分母不由C等式改写。
旧181完整域和28联动帽的Main检查记录保留原SHA与准入次序。

一般K列为S，C-only已消等式的K列为s/5；来源中原有消元原样保留，
本次装配不增加消元。来源的末BR均值真权是1；新增数值正除数25，
源IC实际权可变化，不能误当数值除数。旧1586行字典及全部正尺度逐字保留。
完整513非负变量、两条等式、30条rhs=−1及独立K均保留。
准入事实是原模型必要行，不是完整SPE可实现性或half结论。
''')
    release.update(status='MAIN_RELEASED_COMPLETE_SOURCE_ASSEMBLY',assembly_authorized=True,
                   optimizer_authorized=False,freeze_authorized=False,
                   final_source_review_complete=True,final_source_review_sha256=h(old),
                   final_raw_count=3056)
    release['pending_source_decisions']={
       'source2_minimal_cap_safe':{'include':True,'package':'source2_minimal_cap_safe','main_reason':'完整28个C-only顶点；保留负自由等式乘子。'},
       'all_source_minimal_cap_safe':{'include':True,'package':'all_source_minimal_cap_safe','main_reason':'五源完整137顶点×8合法纯目标，保留全部1096行。'},
       'ordered_minimal_cap_menu':{'include':True,'package':'ordered_minimal_cap','main_reason':'完整q0=1/5新域137顶点，无损仿射菜单族。'}}
    release.pop('pending_append_sources_unordered',None)
    release['main_checksum_verification']=checksum_counts
    assert 1586+sum(s['raw_count'] for s in release['append_sources'])==3056
    write(P/'final_release.json',release)
    print(json.dumps({'status':release['status'],'raw_rows':3056,'optimizer_authorized':False,
                      'final_release_sha256':h(P/'final_release.json'),'checksum_entries':checksum_counts},ensure_ascii=False))
if __name__=='__main__':main()

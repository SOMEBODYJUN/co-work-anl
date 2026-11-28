"""Re-extract cited NFRA cells, preserving dates, units, source versions and display precision."""
import csv
import hashlib
from pathlib import Path
from urllib.request import urlopen

import xlrd

HERE = Path(__file__).resolve().parent
BASE = 'https://www.nfra.gov.cn/chinese/docfile/'
# Published attachment IDs are pinned. The government document ID is reused across quarters.
FILES = [
    ('BK001',2026,'group','by_type.xls','2026/0869d091f08a4595b11993e67d078bec.xls','d713257c8e5ec4deab3fa18831e97798daa0c41fe3beb8dc33f7815275de2edc'),
    ('BK002',2026,'all','industry.xls','2026/6d1e47e848fa4450953468bf55f9e0e2.xls','03c73e414371b437c12e8e95a70c03d9a17b9bf0a76a74c19979ca614d957e15'),
    ('BK010',2025,'group','1208455.xls','2026/cf39fbf37cef40b6aef93ada53465401.xls','a33c3dfe7da199ecc4bed83819f8f5e08de3c5d791c60e25402d401890cdcf15'),
    ('BK011',2025,'all','1208453.xls','2026/9a20b3d34d24444bbdd77a210675a95c.xls','207e58f1e78a59c2452391966e974121691c959bc90347aebbb62e4a61f3254e'),
    ('BK012',2024,'group','1164262.xls','2025/223cf1019c794500b0f361a2fe1bf5d4.xls','4fcc62a3d4740e1571fca69fb0c1678f0e6ac2016305ae9141eb736fe5ac9b54'),
    ('BK013',2024,'all','1164263.xls','2025/19c05ee018b748708a7ae6e67311eba8.xls','921c5301958e687142cbfc21bb227abfbcf03d9a882db9be977fe5bbcd257404'),
]
GROUP = {0:'不良贷款余额',4:'不良贷款率',5:'资产利润率',6:'拨备覆盖率',7:'资本充足率',8:'流动性比例',9:'净利润',10:'净息差'}
ALL = {6:'正常类贷款',7:'关注类贷款',8:'不良贷款余额',13:'关注类贷款占比',14:'不良贷款率',18:'贷款损失准备',19:'拨备覆盖率',20:'贷款拨备率',22:'流动性比例',25:'流动性覆盖率',26:'净稳定资金比例',28:'净利润',29:'资产利润率',30:'资本利润率',31:'净息差',35:'核心一级资本净额',36:'一级资本净额',37:'资本净额',41:'风险加权资产合计',42:'核心一级资本充足率',43:'一级资本充足率',44:'资本充足率'}
RATIOS = {'不良贷款率','关注类贷款占比','资产利润率','资本利润率','净息差','拨备覆盖率','贷款拨备率','资本充足率','核心一级资本充足率','一级资本充足率','流动性比例','流动性覆盖率','净稳定资金比例'}


def output_row(sheet, source, year, quarter, group, metric, row, column):
    value = sheet.cell_value(row, column)
    if value == '':
        return None
    unit = '百分比' if metric in RATIOS else '亿元'
    # Preserve the stored precision in the last column. Typical official table display is two decimals.
    value_report_units = value * 100 if metric in RATIOS else value
    cell = f'{chr(65+column)}{row+1}'
    return [source,year,quarter,group,metric,unit,round(value_report_units,9),sheet.name,cell]


def main():
    rows=[]
    for source, year, kind, name, url, expected_hash in FILES:
        cache=HERE/'cache'/name
        data=cache.read_bytes() if cache.exists() else urlopen(BASE+url,timeout=30).read()
        if hashlib.sha256(data).hexdigest()!=expected_hash:
            raise ValueError(f'Changed source bytes for {source}')
        sheet=xlrd.open_workbook(file_contents=data).sheet_by_index(0)
        for q in range(1,5):
            if kind=='group':
                for offset,metric in GROUP.items():
                    row=4+(q-1)*11+offset
                    if metric not in sheet.cell_value(row,1):
                        raise ValueError((source,metric,row))
                    for column in range(2,8):
                        group=sheet.cell_value(2,column).replace('\n','')
                        rows.append(output_row(sheet,source,year,q,group,metric,row,column))
            else:
                for row,metric in ALL.items():
                    label=sheet.cell_value(row-1,0)
                    # The older template has separate sub-rows for risk types, verified by labels.
                    if metric not in label:
                        raise ValueError((source,metric,label,row))
                    rows.append(output_row(sheet,source,year,q,'商业银行合计',metric,row-1,q))
    with (HERE/'regulatory_series.csv').open('w',newline='',encoding='utf-8') as out:
        writer=csv.writer(out)
        writer.writerow(['source_id','year','quarter','bank_group','metric','unit','value','sheet','cell'])
        writer.writerows(row for row in rows if row is not None)


if __name__=='__main__':
    main()

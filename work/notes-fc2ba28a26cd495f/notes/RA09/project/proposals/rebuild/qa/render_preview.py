import re,subprocess,json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
(HERE/'tmp').mkdir(exist_ok=True)
os.environ['TMPDIR']=str(HERE/'tmp')
body=(HERE.parent/'study-notes.md').read_text()
body=re.sub(r'<!-- unit: ([^ ]+) -->',r'<div id="\1"></div>',body)
body=re.sub(r'^> \[!info\] (.*)$',r'> **\1**\n>',body,flags=re.M)
body=body.replace('../../crops/','../../../crops/')
(HERE/'study-preview.md').write_text(body)
css='''<style>body{max-width:1050px;margin:38px auto;padding:0 26px;font-family:"Noto Sans CJK SC","Noto Sans",sans-serif;line-height:1.7;color:#20252b;font-size:17px;}h1,h2,h3{line-height:1.4}blockquote{margin:20px 0;padding:17px 23px;background:#edf5ff;border-left:4px solid #2878c7;color:#15558b;border-radius:4px;}blockquote p:first-child{margin-top:0}blockquote p:last-child{margin-bottom:0}math[display="block"]{margin:14px auto;overflow-x:auto;}table{border-collapse:collapse;width:100%;font-size:16px;}th,td{padding:7px 10px;border:1px solid #a6bfd5}img{max-width:100%;height:auto;}a{color:#175fa5}#title-block-header{display:none}</style>'''
(HERE/'style.html').write_text(css)
proc=subprocess.run(['pandoc',str(HERE/'study-preview.md'),'-f','markdown+tex_math_dollars','-t','html5','--mathml','--standalone','--metadata','title=实分析9复习稿排版预览','--include-in-header',str(HERE/'style.html'),'-o',str(HERE/'study-preview.html')],capture_output=True,text=True)
(HERE/'pandoc-render.log').write_text((proc.stdout+proc.stderr).rstrip()+'\n')
assert proc.returncode==0,proc.stderr
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1200,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((HERE/'study-preview.html').as_uri());page.evaluate('document.fonts.ready')
 report={'preview':'Pandoc MathML with local callout styling; does not substitute for Obsidian or mathematical review','math_count':page.locator('math').count(),'page_errors':errors,'screenshots':[]}
 for anchor,name in [('N-P002-S03','preview-m001.png'),('N-P009-S01','preview-four-conditions.png'),('N-P010-S01','preview-indicator.png')]:
  page.locator('#'+anchor).evaluate('(el)=>el.scrollIntoView({block:"start"})')
  page.screenshot(path=str(HERE/name),full_page=False)
  report['screenshots'].append({'anchor':anchor,'path':name})
 report['body_scroll_width']=page.evaluate('document.body.scrollWidth');report['viewport_width']=1200
 (HERE/'render-metrics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2).rstrip()+'\n')
 browser.close()
print(json.dumps(report,ensure_ascii=False))

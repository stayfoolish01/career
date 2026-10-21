import json,re,csv
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from collect import ROOT,fetch

rows=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
urls=[
'https://career.studying.jp/policy?policy_no=6',
'https://career.studying.jp/column/scout',
'https://career.studying.jp/column/careersupport',
'https://career.studying.jp/inquiry',
'https://career.studying.jp/member-inquiry',
'https://career.studying.jp/robots.txt',
'https://career.studying.jp/sitemap.xml',
]
for r in rows:
    if r['id']=='S01':
        urls += [a['url'] for a in r['links'] if '/jobs/' in a['url']][:2]
        urls += [a['url'] for a in r['links'] if a['text'] in ['東京都','経理','転職ノウハウ']][:3]
    if r['id']=='S07':
        urls += [a['url'] for a in r['links'] if '/column/agent/' in a['url']]
        urls += [a['url'] for a in r['links'] if re.search(r'/kyujin/\d+$',a['url'])][:3]
urls=list(dict.fromkeys(urls))
extra=list(ThreadPoolExecutor(max_workers=4).map(fetch,[(f'S{i+12:02}',u) for i,u in enumerate(urls)]))
rows+=extra
for r in extra:
    if r.get('status')==200 and '/jobs/' in r['url']:
        jobs=list(dict.fromkeys(a['url'] for a in r.get('links',[]) if re.search(r'/kyujin/\d+$',a['url'])))[:5]
        rows+=list(ThreadPoolExecutor(max_workers=3).map(fetch,[(f'S{len(rows)+i+1:02}',u) for i,u in enumerate(jobs)]))
(ROOT/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','title','url','final_url','status','retrieved_at_utc','sha256','error'],extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps([{k:r.get(k) for k in ('id','status','title','url','error')} for r in rows[11:]],ensure_ascii=False))

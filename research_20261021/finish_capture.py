import json,re,csv,hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from collect import ROOT,fetch

rows=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
urls=[]
for r in rows:
    if r['id'] in ['S20','S21']:
        urls+=list(dict.fromkeys(a['url'] for a in r['links'] if re.search(r'/kyujin/\d+$',a['url'])))[:3]
    if r['id']=='S14':
        urls += [a['url'] for a in r['links'] if any(t in a['text'] for t in ['申し込む','申し込みフォーム']) and a['url'].startswith('https://')][:1]
urls=list(dict.fromkeys(urls))
rows+=list(ThreadPoolExecutor(max_workers=4).map(fetch,[(f'S{i+69:02}',u) for i,u in enumerate(urls)]))
(ROOT/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','title','url','final_url','status','retrieved_at_utc','sha256','error'],extrasaction='ignore');w.writeheader();w.writerows(rows)
fields=[]
for r in rows:
    if r.get('status')!=200:continue
    soup=BeautifulSoup((ROOT/'sources'/f"{r['id']}.html").read_bytes(),'html.parser')
    for n in soup.select('input,select,textarea'):
        if n.get('type') in ['hidden','password']: continue
        label=soup.find('label',attrs={'for':n.get('id')}) if n.get('id') else None
        label=label or n.find_parent('label')
        fields.append({'source':r['id'],'name':n.get('name',''),'type':n.get('type',n.name),'value':n.get('value','') if n.get('type') in ['radio','checkbox'] else '', 'label':label.get_text(' ',strip=True) if label else '', 'options':' / '.join(o.get_text(' ',strip=True) for o in n.select('option'))})
with (ROOT/'form_fields.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['source','name','type','value','label','options']);w.writeheader();w.writerows(fields)
assets=[]
for r in rows:
    if r['id'] in ['S02','S03','S05','S13','S14']:
        assets += [i['url'] for i in r.get('images',[]) if urlparse(i['url']).hostname in ['careerwp.studying.jp','d38pwhfwpp36sx.cloudfront.net']]
assets=list(dict.fromkeys(assets))
(ROOT/'assets').mkdir(exist_ok=True)
def asset(url):
    name=hashlib.sha256(url.encode()).hexdigest()[:12]+(PathSuffix(url))
    try:
        r=requests.get(url,timeout=20)
        if r.status_code==200:(ROOT/'assets'/name).write_bytes(r.content)
        return {'url':url,'file':name,'status':r.status_code,'sha256':hashlib.sha256(r.content).hexdigest()}
    except Exception as e:return {'url':url,'error':str(e)}
def PathSuffix(url):
    from pathlib import Path
    return Path(urlparse(url).path).suffix or '.bin'
ar=list(ThreadPoolExecutor(max_workers=4).map(asset,assets))
(ROOT/'assets_manifest.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'sources':len(rows),'successful':sum(r.get('status')==200 for r in rows),'assets':len(ar),'assets_ok':sum(r.get('status')==200 for r in ar),'new_sources':[{k:r.get(k) for k in ['id','url','title','status']} for r in rows[68:]]},ensure_ascii=False))

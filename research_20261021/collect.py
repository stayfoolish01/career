from pathlib import Path
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import requests, json, hashlib, csv
from datetime import datetime, timezone
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
(ROOT/'sources').mkdir(exist_ok=True)
SEEDS = [
('S01','https://career.studying.jp/'),
('S02','https://studying.jp/career_release.html'),
('S03','https://career.studying.jp/column/about'),
('S04','https://career.studying.jp/column/faq'),
('S05','https://career.studying.jp/column/corporation'),
('S06','https://career.studying.jp/kyujin/search-detail'),
('S07','https://career.studying.jp/column/agent-list'),
('S08','https://career.studying.jp/policy?policy_no=7'),
('S09','https://career.studying.jp/contents/accessibility'),
('S10','https://career.studying.jp/mypage/login'),
('S11','https://member.studying.jp/career/signup/'),
]

def fetch(item):
    sid,url=item
    row={'id':sid,'url':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
    try:
        r=requests.get(url,timeout=35)
        r.encoding=r.apparent_encoding
        row.update(status=r.status_code,final_url=r.url,sha256=hashlib.sha256(r.content).hexdigest())
        (ROOT/'sources'/f'{sid}.html').write_bytes(r.content)
        soup=BeautifulSoup(r.text,'html.parser')
        row['title']=soup.title.get_text(' ',strip=True) if soup.title else ''
        row['links']=[{'text':a.get_text(' ',strip=True),'url':urljoin(r.url,a['href'])} for a in soup.select('a[href]')]
        row['images']=[{'alt':a.get('alt',''),'url':urljoin(r.url,a.get('src',''))} for a in soup.select('img[src]')]
        row['forms']=[{'action':urljoin(r.url,f.get('action','')),'method':f.get('method','get'),'fields':[{'tag':i.name,**{k:i.get(k) for k in ('name','type','value','placeholder','required') if i.has_attr(k)},'options':[o.get_text(' ',strip=True) for o in i.select('option')]} for i in f.select('input,select,textarea')]} for f in soup.select('form')]
        for x in soup.select('script,style,noscript'):x.decompose()
        (ROOT/'sources'/f'{sid}.txt').write_text(soup.get_text('\n',strip=True),encoding='utf-8')
    except Exception as e:row['error']=str(e)
    return row

if __name__=='__main__':
    rows=list(ThreadPoolExecutor(max_workers=4).map(fetch,SEEDS))
    (ROOT/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps([{k:r.get(k) for k in ('id','status','title','error')} for r in rows],ensure_ascii=False))

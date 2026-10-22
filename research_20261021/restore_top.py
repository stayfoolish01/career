"""Restore saved homepage markup with locally cached display assets."""
from pathlib import Path
from urllib.parse import urljoin,urlparse
import hashlib,json,re,requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'top_restored'
(OUT/'assets').mkdir(parents=True,exist_ok=True)
BASE='https://career.studying.jp/'
records={}
def get_asset(url):
    url=urljoin(BASE,url)
    if url.startswith(('data:','javascript:')):return url
    if url in records:return records[url]['local'] if records[url].get('status')==200 else url
    suffix=Path(urlparse(url).path).suffix or '.bin'
    name=hashlib.sha256(url.encode()).hexdigest()[:20]+suffix
    row={'url':url,'local':'assets/'+name,'retrieved_at_utc':datetime.now(timezone.utc).isoformat()}
    records[url]=row
    try:
        r=requests.get(url,timeout=25)
        row['status']=r.status_code
        row['content_type']=r.headers.get('Content-Type','')
        if r.status_code!=200:return url
        if suffix=='.css' or 'text/css' in row['content_type']:
            r.encoding='utf-8'
            def rewrite(m):
                ref=m.group(1).strip(' \"\'')
                if ref.startswith(('data:','#')):return m.group(0)
                loc=get_asset(urljoin(url,ref))
                return 'url("'+(loc.removeprefix('assets/') if loc.startswith('assets/') else loc)+'")'
            data=re.sub(r'url\(([^)]+)\)',rewrite,r.text).encode('utf-8')
        else:data=r.content
        (OUT/row['local']).write_bytes(data)
        row['sha256']=hashlib.sha256(data).hexdigest()
        return row['local']
    except Exception as e:row['error']=str(e);return url

def main():
    soup=BeautifulSoup((ROOT/'sources/S01.html').read_bytes(),'html.parser')
    # Preserve yesterday's markup; disable scripts, tracking, and form submissions.
    for el in soup.select('script,iframe,base'):el.decompose()
    for el in soup.find_all(True):
        for key in list(el.attrs):
            if key.lower().startswith('on'):del el.attrs[key]
    for el in soup.select('input[type=hidden]'):el.decompose()
    for form in soup.select('form'):
        form['action']='#';form['onsubmit']='return false'
    targets=[]
    for el in soup.select('link[href],img[src],input[src]'):
        attr='href' if el.name=='link' else 'src'
        if el.name=='link' and not set(el.get('rel',[]))&{'stylesheet','icon','shortcut'}:continue
        targets.append((el,attr,urljoin(BASE,el[attr])))
    # Fetch independent initial assets; CSS dependencies are fetched recursively.
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(lambda t:get_asset(t[2]),targets))
    for (el,attr,url),local in zip(targets,results):el[attr]=local
    for el in soup.select('[style]'):
        el['style']=re.sub(r'url\(([^)]+)\)',lambda m:'url("'+get_asset(urljoin(BASE,m.group(1).strip(' \"\'')))+'")',el['style'])
    for a in soup.select('a[href]'):
        if not a['href'].startswith(('#','javascript:')):a['href']=urljoin(BASE,a['href'])
    # Restrict rendering to local resources; missing assets remain visibly missing.
    meta=soup.new_tag('meta');meta['http-equiv']='Content-Security-Policy';meta['content']="default-src 'self' data: file:; style-src 'self' 'unsafe-inline' file:; script-src 'unsafe-inline'; form-action 'none'; connect-src 'none'"
    soup.head.insert(0,meta)
    (OUT/'index.html').write_text(str(soup),encoding='utf-8')
    (OUT/'asset_manifest.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'assets':len(records),'success':sum(x.get('status')==200 for x in records.values()),'failed':[x for x in records.values() if x.get('status')!=200]},ensure_ascii=False))

if __name__=='__main__':main()

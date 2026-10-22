"""Create an explicitly approximate visual reconstruction, using saved markup."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re,shutil
from email import policy
from email.parser import BytesParser

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'top_restored';(OUT/'assets').mkdir(exist_ok=True)
soup=BeautifulSoup((ROOT/'sources/S01.html').read_bytes(),'html.parser')
for x in soup.select('script,iframe,base,link'):x.decompose()
for x in soup.find_all(True):
    for a in list(x.attrs):
        if a.lower().startswith('on'):del x.attrs[a]
for x in soup.select('input[type=hidden]'):x.decompose()
for x in soup.select('form'):x['action']='#';x['onsubmit']='return false'
for x in soup.select('a[href]'):
    if not x['href'].startswith('#'):x['href']='#'
for x in soup.select('img'):
    x.attrs.pop('src',None);x.attrs.pop('srcset',None)
    x['class']=x.get('class',[])+['missing-asset']
for p in (ROOT/'assets').glob('*'):shutil.copy2(p,OUT/'assets'/p.name)
for x in soup.select('.logo img'):
    x['src']='assets/c47df15bd2b4.png';x['class']=[]
for x in soup.select('.main-visual img'):
    x['src']='assets/c38a9662f628.jpg';x['class']=[]
    x['alt']='代替画像：同サービスの初めての方向けページから保存した画像'
for x in list(soup.select('img.missing-asset')):
    replacement=soup.new_tag('div');replacement['class']='missing-asset'
    replacement.string='画像原本未取得'+('：'+x.get('alt','') if x.get('alt') else '')
    x.replace_with(replacement)
hero=soup.select_one('.main-visual')
if hero:
    note=soup.new_tag('p');note['class']='asset-note';note.string='メイン画像は原本を取得できないため、同サービスの保存画像で代替しています。';hero.append(note)
# Banner screenshots contain unrelated personal form fields; do not embed them.
for x in soup.select('.modal'):x.decompose()
style=soup.new_tag('link',rel='stylesheet',href='reconstruction.css');soup.head.append(style)
meta=soup.new_tag('meta');meta['http-equiv']='Content-Security-Policy';meta['content']="default-src 'none'; img-src 'self' file: data:; style-src 'self' file: 'unsafe-inline'; script-src 'unsafe-inline'; form-action 'none'";soup.head.insert(0,meta)
notice=soup.new_tag('aside');notice['class']='archive-notice';notice.string='2026年10月21日保存HTMLからの参考再現｜本文・構成は保存データ、CSSは再構成。検索・申込は動作しません。';soup.body.insert(0,notice)
(OUT/'index.html').write_text(str(soup),encoding='utf-8')
(OUT/'再現について.txt').write_text('2026年10月21日21:40 JSTに保存したS01.htmlを使用。2026年10月22日に再構成。\n原CSS・トップ固有画像は取得時点で503。トップの実スクリーンショットはなく、完全一致は確認できない。\n本文とセクション順は保存HTMLを使用。ヘッダー・配色・余白等は他ページのスクリーンショットを参考に再構成。\nメイン画像は初めての方向けページの保存画像で代替。未取得の画像枠は原本未取得と表示。\nスクリプト・計測・フォーム送信・外部遷移は無効。サービスとして利用するものではない。\n元HTMLのフォームトークン・非表示入力は除去。\n',encoding='utf-8')
print('Built',OUT/'index.html')

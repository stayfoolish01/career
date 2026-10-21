from pathlib import Path
import html,re
ROOT=Path(__file__).resolve().parent
def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'<a href="\2">\1</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
lines=(ROOT/'要件定義の基礎調査.md').read_text(encoding='utf-8').splitlines()
out=[]; table=False
for line in lines:
    if line.startswith('|'):
        cells=[x.strip() for x in line.strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?',x) for x in cells):continue
        if not table:out.append('<div class="table"><table>');table=True
        out.append('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in cells)+'</tr>');continue
    if table:out.append('</table></div>');table=False
    if not line.strip():continue
    m=re.match(r'^(#{1,6}) (.*)',line)
    if m:out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>')
    else:out.append('<p>'+inline(line)+'</p>')
if table:out.append('</table></div>')
head='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>スタディングキャリア 基本仕様と要件整理</title><style>body{font:16px/1.85 "Yu Gothic",Meiryo,sans-serif;max-width:1120px;margin:36px auto;padding:0 24px;color:#243244}h1,h2,h3{line-height:1.5;color:#18334f}h2{margin-top:48px;border-bottom:2px solid #e65a16;padding-bottom:8px}table{border-collapse:collapse;width:100%;font-size:14px}td{border:1px solid #cbd5df;padding:10px;vertical-align:top;min-width:110px}tr:first-child{background:#edf2f6;font-weight:bold}.table{overflow:auto}a{color:#0866ad}code{background:#edf2f6;padding:2px 4px}.notice{background:#fff4df;padding:16px} @media print{body{max-width:none;margin:0}h2{break-after:avoid}tr{break-inside:avoid}}</style><p class="notice">ローカル保存版。現行の公開仕様と新システムへの提案を区別して記載しています。追加画像で確認した登録項目は <a href="screenshot_review/登録フォーム確認項目.csv">登録フォーム仕様一覧</a>、画像との対応は <a href="screenshot_review/追加画像の確認.csv">追加画像一覧</a> を参照してください。</p>'''
(ROOT/'基本仕様と要件整理.html').write_text(head+'\n'.join(out)+'</html>',encoding='utf-8')
p=ROOT/'index.html';s=p.read_text(encoding='utf-8');s=s.replace('<a href="要件定義の基礎調査.md">調査報告</a>','<a href="基本仕様と要件整理.html">基本仕様と要件整理 HTML版</a> / <a href="要件定義の基礎調査.md">調査報告 Markdown版</a>');p.write_text(s,encoding='utf-8')
print('HTML report saved')

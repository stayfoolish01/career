"""Bundle the LP into one offline HTML file, without external dependencies."""
from pathlib import Path
import base64
import mimetypes

ROOT = Path(__file__).resolve().parent
html = (ROOT / 'index.html').read_text(encoding='utf-8')
css = (ROOT / 'style.css').read_text(encoding='utf-8')
js = (ROOT / 'app.js').read_text(encoding='utf-8')
html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + css + '</style>')
html = html.replace('<script src="app.js" defer></script>', '')
html = html.replace('</body>', '<script>' + js.replace('</script', '<\\/script') + '</script></body>')
for filename in ['assets/logo.png', 'assets/career.jpg']:
    path = ROOT / filename
    mime = mimetypes.guess_type(path.name)[0]
    data = base64.b64encode(path.read_bytes()).decode('ascii')
    html = html.replace('src="' + filename + '"', 'src="data:' + mime + ';base64,' + data + '"')
policy = "default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; form-action 'none'; base-uri 'none'"
html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="' + policy + '">')
out = ROOT / 'スタディングキャリア_共有用.html'
out.write_text(html, encoding='utf-8')
print(f'Built {out.name}: {out.stat().st_size:,} bytes')

"""Build the strictly allowlisted public showcase, never the private implementation."""
import json
from pathlib import Path
import re
import shutil
import html
from render_brand import render

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
PUBLIC_FILES = {'index.html','methodology.html','style.css','app.js','data/results.json','assets/mark.svg','assets/aegis-orbit.svg','assets/aegis-pipeline.svg','assets/aegis-gauntlet.svg','assets/historical-highlights.svg'}


def reject_link(path):
    if path.is_symlink() or path.is_junction():
        raise ValueError('Linked publication path is forbidden')


def build():
    for p in [PUBLIC,*PUBLIC.rglob('*')]: reject_link(p)
    data=render()
    rows=''.join(f'<tr><th scope="row">{html.escape(r["title"])}</th><td>{r["inception"]} – {r["last_mark"]}</td><td>{r["mode"]}</td><td>+{r["return_pct"]:.3f}%</td><td>+{r["benchmark_return_pct"]:.3f}%</td></tr>' for r in data['rows'])
    page=PUBLIC/'index.html'
    body,count=re.subn(r'(?s)(<tbody id="result-rows">).*?(</tbody>)',lambda m:m[1]+rows+m[2],page.read_text(encoding='utf-8'))
    if count!=1: raise ValueError('Historical table marker missing')
    page.write_text(body,encoding='utf-8',newline='\n')
    files=[p for p in PUBLIC.rglob('*') if p.is_file()]
    actual={p.relative_to(PUBLIC).as_posix() for p in files}
    if actual!=PUBLIC_FILES: raise ValueError(f'Publish allowlist mismatch: extra={actual-PUBLIC_FILES}; missing={PUBLIC_FILES-actual}')
    for p in files:
        if p.suffix not in {'.html','.css','.js','.svg'}: continue
        text=p.read_text(encoding='utf-8')
        for link in re.findall(r'(?:src|href)="(/[^"?#]*)',text):
            if not (PUBLIC/(link.lstrip('/') or 'index.html')).exists(): raise ValueError(f'Broken local link: {link}')
    output=ROOT/'.vercel/output';static=output/'static'
    for p in [ROOT/'.vercel',output,static]: reject_link(p)
    if static.resolve()!=ROOT/'.vercel/output/static': raise ValueError('Output path escaped')
    if static.exists(): shutil.rmtree(static)
    static.mkdir(parents=True)
    for source in files:
        destination=static/source.relative_to(PUBLIC);destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
    headers={'X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"}
    (output/'config.json').write_text(json.dumps({'version':3,'routes':[{'src':'/(.*)','headers':headers,'continue':True},{'handle':'filesystem'},{'src':'/','dest':'/index.html'}]},indent=2),encoding='utf-8')
    print(json.dumps({'public_files':len(files),'historical_mark':data['last_market_mark'],'original_brand':'orbit + blackline','output':str(output)}))


if __name__=='__main__': build()

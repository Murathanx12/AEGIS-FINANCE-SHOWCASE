"""Reuse the original orbit/blackline renderer with dated, curated public data."""
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape
import brand_renderer as original

ROOT = Path(__file__).resolve().parents[1]


def results_svg(data):
    bar_css = '.result-bar{transform-box:fill-box;transform-origin:left center;animation:result-reveal 1.4s cubic-bezier(.2,.8,.2,1) both}@keyframes result-reveal{from{transform:scaleX(0)}to{transform:scaleX(1)}}'
    out = original._head(1200, 470, 'Aegis: historical paper highlights, 9 October 2026', data['selection'], original._results_css() + bar_css) + [ '<rect width="1200" height="470" class="bg"/>', '<text x="40" y="40" class="sec">SELECTED HISTORICAL PAPER HIGHLIGHTS</text>', '<text x="1160" y="40" text-anchor="end" class="secr">MARKS 09 OCT 2026</text>', '<path d="M40 58H1160" class="rule"/>']
    for i, row in enumerate(data['rows']):
        x = 40 + 385 * i
        out.extend([
            f'<path d="M{x+12} 86H{x}V98m338-12h12v12M{x} 366v12h12m326 0h12v-12" fill="none" stroke="rgba(255,255,255,.6)"/>',
            f'<text x="{x+20}" y="125" class="acct">{escape(row["title"])}</text>',
            f'<text x="{x+20}" y="178" class="excess">+{row["return_pct"]:.3f}%</text>',
            f'<text x="{x+20}" y="201" class="exlab">HISTORICAL {row["mode"].upper()} RETURN</text>',
            f'<text x="{x+20}" y="235" class="meta">{row["inception"]} to {row["last_mark"]}</text>',
            f'<text x="{x+20}" y="256" class="badge">{escape(row["label"])} · OWN-WINDOW SPY</text>'])
        for j, (value, css, label) in enumerate([(row['return_pct'], 'bar-acct', 'Account'), (row['benchmark_return_pct'], 'bar-spy', 'SPY')]):
            y = 285 + j * 28
            width = value / 12 * 205
            out.append(f'<text x="{x+20}" y="{y+7}" class="meta">{label}</text><rect x="{x+85}" y="{y}" width="205" height="7" class="track"/><rect x="{x+85}" y="{y}" width="{width:.2f}" height="7" class="{css} result-bar"/><text x="{x+299}" y="{y+7}" class="valspy">+{value:.3f}%</text>')
        out.append(f'<text x="{x+20}" y="352" class="meta">+{row["excess_pp"]:.3f} pp versus SPY</text>')
    out.extend(['<text x="40" y="416" class="fine">Three positive examples selected after the fact from 307 benchmark-comparable accounts; not the whole record.</text>', '<text x="40" y="438" class="fine">Historical paper only, not current performance. Different windows; simulator and broker evidence are separate.</text>', '<text x="40" y="458" class="fine">Hack2: actual series available for 10/30 sessions. Source: roi_2026-10-10T235231Z. Read the methodology.</text>', '</svg>'])
    return '\n'.join(out) + '\n'


def render():
    data = json.loads((ROOT / 'public/data/results.json').read_text(encoding='utf-8'))
    if data['kind'] != 'selected-historical-paper-highlights' or data['is_live_feed']:
        raise ValueError('Only the explicitly dated historical highlight packet may be rendered')
    if len(data['rows']) != 3 or data['benchmark_comparable_accounts'] != 307:
        raise ValueError('Historical selection scope mismatch')
    for row in data['rows']:
        if row['last_mark'] != data['last_market_mark'] or row['return_pct'] <= 0:
            raise ValueError('Unexpected historical highlight')
        if abs(row['return_pct'] - row['benchmark_return_pct'] - row['excess_pp']) > .0011:
            raise ValueError('Benchmark arithmetic mismatch')
    outputs = {'aegis-orbit.svg': original.render_hero().replace('OPEN SOURCE', 'PUBLIC VIEW').replace('LOOP RUNNING', 'SYSTEM MODEL'), 'aegis-pipeline.svg': original.render_pipeline(), 'aegis-gauntlet.svg': original.render_gauntlet(), 'historical-highlights.svg': results_svg(data)}
    for name, value in outputs.items():
        # SMIL does not honor CSS animation:none. Hide its decorative moving
        # circle in the still frame, keeping the real path and all labels.
        value = re.sub(r'(<circle\b[^>]*)(>\s*<animateMotion\b)',
                       lambda m: m[1] + ' class="smil-motion"' + m[2], value)
        value = value.replace('</style>', '@media(prefers-reduced-motion:reduce){.pulse,.comet,.smil-motion{display:none!important}}</style>')
        (ROOT / 'public/assets' / name).write_text(value, encoding='utf-8', newline='\n')
    return data


if __name__ == '__main__':
    render()

"""Build only the curated public tree; render the dated snapshot deterministically."""
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PUBLIC_FILES = {
    "index.html", "methodology.html", "style.css", "app.js",
    "data/results.json", "assets/research-loop.svg", "assets/mark.svg",
    "assets/paper-comparison.svg",
}


def reject_links(directory):
    # A linked parent directory can leak files even when each child is not a link.
    for path in [directory, *directory.rglob("*")]:
        if path.is_symlink() or path.is_junction():
            raise ValueError(f"Linked publish path is forbidden: {path}")


def signed(value):
    return f"{value:+.3f}%".replace("-", "−")


def render():
    data = json.loads((PUBLIC / "data/results.json").read_text(encoding="utf-8"))
    assert data["kind"] == "forward-paper-observation" and not data["is_live_feed"]
    cohort = data["cohort"]
    assert cohort["ahead_of_spy"] + cohort["behind_spy"] == cohort["benchmark_comparable"]
    rows = data["rows"]
    assert len({r["account"] for r in rows}) == len(rows) == 5
    for r in rows:
        assert abs((r["end_nav"] / r["start_nav"] - 1) * 100 - r["return_pct"]) < .00051
        assert abs(r["return_pct"] - r["benchmark_return_pct"] - r["excess_pp"]) < .0011
        assert r["maximum_drawdown_pct"] is None
    table = "".join(
        f'<tr><th scope="row">{html.escape(r["account"])}</th><td>{dt.date.fromisoformat(r["inception"]).strftime("%d %b %Y")}</td><td>{signed(r["return_pct"])}</td><td>{signed(r["benchmark_return_pct"])}</td></tr>'
        for r in rows
    )
    page = PUBLIC / "index.html"
    original = page.read_text(encoding="utf-8")
    updated, count = re.subn(r'(?s)(<tbody id="result-rows">).*?(</tbody>)', lambda m: m[1] + table + m[2], original)
    assert count == 1
    page.write_text(updated, encoding="utf-8")
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="490" viewBox="0 0 1000 490" role="img" aria-labelledby="title desc">',
           '<title id="title">Selected forward paper results through 16 October 2026</title><desc id="desc">Five account endpoints, each with its own inception date and matching SPY return. Selected after observing outcomes. Cohort20 ahead,287 behind among307 comparable accounts. Paper only, not a time series.</desc>',
           '<rect width="1000" height="490" fill="#edf3f8"/>',
           '<g font-family="Segoe UI,Arial,sans-serif" fill="#102638">',
           '<text x="0" y="27" font-size="20">Return from each account’s own start (%)</text>',
           '<circle cx="22" cy="57" r="5" fill="#245bb0"/><text x="37" y="62" font-size="15">Paper account</text>',
           '<path d="M190 52h10v10h-10Z" fill="#9c5b19"/><text x="210" y="62" font-size="15">SPY over the matching window</text>']
    x = lambda value: 235 + (value + 36) / 46 * 625
    for tick in [-30, -20, -10, 0, 10]:
        tx = x(tick)
        svg.append(f'<path d="M{tx:.2f} 95V415" stroke="{"#8fa7b9" if tick == 0 else "#c9d6e0"}"/><text x="{tx:.2f}" y="449" text-anchor="middle" font-size="15" fill="#4e6574">{tick:+d}%</text>')
    for i, r in enumerate(rows):
        y = 117 + i * 67
        a, b = x(r["return_pct"]), x(r["benchmark_return_pct"])
        svg.append(f'<text x="0" y="{y}" font-size="17">{html.escape(r["account"])}</text><text x="0" y="{y+22}" font-size="13" fill="#4e6574">Since {r["inception"]}</text>')
        svg.append(f'<path d="M{a:.2f} {y}H{b:.2f}" stroke="#8fa7b9" stroke-width="2"/><circle cx="{a:.2f}" cy="{y}" r="6" fill="#245bb0"/><rect x="{b-5:.2f}" y="{y-5}" width="10" height="10" fill="#9c5b19"/>')
        svg.append(f'<text x="884" y="{y+5}" font-size="17" fill="#245bb0">{signed(r["return_pct"])}</text>')
    svg.append('<text x="0" y="484" font-size="13" fill="#4e6574">Dated endpoint observations · paper only · different windows · selected after the fact</text></g></svg>')
    (PUBLIC / "assets/paper-comparison.svg").write_text("".join(svg), encoding="utf-8")


def build():
    reject_links(PUBLIC)
    render()
    # Check the publish boundary before copying; profiles, private documents and raw
    # inputs are never a source directory for this build.
    files = sorted(p for p in PUBLIC.rglob("*") if p.is_file() and p.relative_to(PUBLIC).as_posix() != "data/.gitkeep")
    actual = {p.relative_to(PUBLIC).as_posix() for p in files}
    if actual != PUBLIC_FILES:
        raise ValueError(f"Publish allowlist mismatch: extra={actual-PUBLIC_FILES}, missing={PUBLIC_FILES-actual}")
    for p in files:
        if p.suffix not in {".html", ".css", ".js", ".svg"}:
            continue
        body = p.read_text(encoding="utf-8")
        for local in re.findall(r'(?:src|href)="(/[^"?#]*)', body):
            assert (PUBLIC / (local.lstrip("/") or "index.html")).exists(), (p, local)
    output = ROOT / ".vercel/output"
    static = output / "static"
    # Replace the publish tree so an artifact removed from public/ cannot survive
    # into a later prebuilt deployment. Verify every ancestor and the absolute
    # deletion target before this bounded recursive removal.
    for path in [ROOT / ".vercel", output, static]:
        if path.is_symlink() or path.is_junction():
            raise ValueError(f"Linked output path is forbidden: {path}")
    if static.resolve() != ROOT / ".vercel" / "output" / "static":
        raise ValueError(f"Unexpected output target: {static}")
    if static.exists():
        shutil.rmtree(static)
    static.mkdir(parents=True, exist_ok=True)
    for source in files:
        destination = static / source.relative_to(PUBLIC)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    (output / "config.json").write_text(json.dumps({"version": 3, "routes": [
        {"src": "/(.*)", "headers": {"X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin", "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"}, "continue": True},
        {"handle": "filesystem"}, {"src": "/", "dest": "/index.html"}
    ]}, indent=2), encoding="utf-8")
    print(json.dumps({"files": len(files), "output": str(output), "snapshot_sha256": hashlib.sha256((PUBLIC / "data/results.json").read_bytes()).hexdigest()}))


if __name__ == "__main__":
    build()

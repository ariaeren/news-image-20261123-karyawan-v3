#!/usr/bin/env python3
"""Render the news entry and its make.fun guide-page capture, offline.

entry.png is produced from the unchanged HTML below. screenshot.png is a
separate 1200x1700 capture of a local guide page written under /root/; its
referral link is read from the kit-generated JSON and is never printed.
"""

import html as html_lib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
WIDTH = 1024
HEIGHT = 1024
GUIDE_HTML = Path("/root/news-image-20261123-guide.html")
REFERRAL_JSON = Path("/root/news-image-20261123-referral.json")
GUIDE_WIDTH = 1200
GUIDE_HEIGHT = 1700
BADGES = (
    ("make.fun · news-image-20261123", "https://make.fun/badge/news-image-20261123.svg"),
    ("rank", "https://make.fun/badge/news-image-20261123/ariaeren/news-image-20261123-karyawan-v3/rank.svg"),
    ("reward", "https://make.fun/badge/news-image-20261123/ariaeren/news-image-20261123-karyawan-v3/reward.svg"),
)

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>World news · 23 November 2026</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  html, body { width: 1024px; height: 1024px; margin: 0; overflow: hidden; }
  body { background: #050912; }
  .page {
    position: relative;
    width: 1024px;
    height: 1024px;
    padding: 38px 42px 34px;
    color: #f4f7fc;
    font-family: "DejaVu Sans", Arial, sans-serif;
    background:
      radial-gradient(circle at 82% 4%, rgba(63,105,181,.28), transparent 34%),
      radial-gradient(circle at 6% 96%, rgba(25,82,105,.20), transparent 36%),
      linear-gradient(160deg, #0b1324 0%, #070c17 58%, #050912 100%);
  }
  .page::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px);
    background-size: 48px 48px;
    -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,.8), transparent 80%);
    mask-image: linear-gradient(to bottom, rgba(0,0,0,.8), transparent 80%);
    pointer-events: none;
  }
  .globe {
    position: absolute;
    right: -46px;
    top: -42px;
    width: 310px;
    height: 310px;
    opacity: .18;
    pointer-events: none;
  }
  .header { position: relative; height: 168px; z-index: 1; }
  .eyebrow {
    font-size: 20px;
    line-height: 1;
    font-weight: 700;
    letter-spacing: 5px;
    color: #8fa8d2;
  }
  .date {
    margin: 14px 0 0;
    font-size: 56px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -2.2px;
    white-space: nowrap;
  }
  .date .dot { color: #ff6b5e; }
  .strip { margin-top: 16px; display: flex; align-items: center; gap: 16px; }
  .bar {
    flex: 1;
    height: 4px;
    border-radius: 3px;
    background: linear-gradient(90deg,
      #ff6b5e 0 16.6%, #f0b64a 16.6% 33.3%, #5aa9ff 33.3% 50%,
      #9b7bff 50% 66.6%, #35d2b0 66.6% 83.3%, #6fd36a 83.3%);
  }
  .strip-label {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2.4px;
    color: #9fb2d1;
    white-space: nowrap;
  }
  .grid {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-template-rows: repeat(3, minmax(0, 1fr));
    gap: 16px;
    height: 772px;
  }
  .card {
    --accent: #fff;
    --glow: rgba(255,255,255,.10);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(164,188,228,.18);
    border-left: 9px solid var(--accent);
    border-radius: 16px;
    padding: 20px 22px 18px 24px;
    background: linear-gradient(135deg, rgba(22,31,51,.97), rgba(10,16,30,.97));
    box-shadow: 0 14px 30px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .card::after {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    right: -70px;
    top: -90px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--glow), transparent 68%);
    pointer-events: none;
  }
  .kicker {
    position: relative;
    z-index: 1;
    margin-bottom: 11px;
    font-size: 17px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: 2.6px;
    color: var(--accent);
    text-transform: uppercase;
  }
  .headline {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: 36px;
    line-height: 1.03;
    font-weight: 800;
    letter-spacing: -1.1px;
  }
  .detail {
    position: relative;
    z-index: 1;
    margin: 13px 0 0;
    font-size: 24px;
    line-height: 1.15;
    font-weight: 500;
    letter-spacing: -.6px;
    color: #d4deef;
    white-space: nowrap;
  }
  .num {
    position: absolute;
    z-index: 1;
    right: 18px;
    top: 17px;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 1px;
    color: rgba(210,224,247,.28);
  }
  .footer {
    position: absolute;
    z-index: 1;
    left: 42px;
    right: 42px;
    bottom: 11px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #7186aa;
  }
  .footer .mark { color: #a8bbda; }
</style>
</head>
<body>
  <main class="page">
    <svg class="globe" viewBox="0 0 240 240" aria-hidden="true">
      <g fill="none" stroke="#9ec1ff" stroke-width="2">
        <circle cx="120" cy="120" r="96"/>
        <ellipse cx="120" cy="120" rx="96" ry="36"/>
        <ellipse cx="120" cy="120" rx="96" ry="68"/>
        <ellipse cx="120" cy="120" rx="36" ry="96"/>
        <ellipse cx="120" cy="120" rx="68" ry="96"/>
        <path d="M25 120H215M120 25V215"/>
      </g>
      <g fill="#9ec1ff" opacity=".8">
        <circle cx="70" cy="80" r="3"/>
        <circle cx="168" cy="96" r="3"/>
        <circle cx="136" cy="171" r="3"/>
      </g>
    </svg>

    <header class="header">
      <div class="eyebrow">WORLD NEWS · DAILY BRIEF</div>
      <h1 class="date">MONDAY <span class="dot">·</span> 23 NOVEMBER 2026</h1>
      <div class="strip">
        <div class="strip-label">SIX STORIES</div>
        <div class="bar"></div>
        <div class="strip-label">ONE DAY</div>
      </div>
    </header>

    <section class="grid">
      <article class="card" style="--accent:#ff6b5e;--glow:rgba(255,107,94,.18)">
        <div class="num">01</div>
        <div class="kicker">CENTRAL UKRAINE</div>
        <h2 class="headline">UKRAINE · Zelenskyy's hometown hit</h2>
        <p class="detail">Missiles kill 2, wound dozens</p>
      </article>

      <article class="card" style="--accent:#f0b64a;--glow:rgba(240,182,74,.18)">
        <div class="num">02</div>
        <div class="kicker">INDONESIA · FIRE</div>
        <h2 class="headline">INDONESIA · Weekend factory fire</h2>
        <p class="detail">24 dead; about 30 missing</p>
      </article>

      <article class="card" style="--accent:#5aa9ff;--glow:rgba(90,169,255,.18)">
        <div class="num">03</div>
        <div class="kicker">US · MARKETS</div>
        <h2 class="headline">US MARKETS · Stocks sell off</h2>
        <p class="detail">S&amp;P 500 -3.7%; Nasdaq down YTD</p>
      </article>

      <article class="card" style="--accent:#9b7bff;--glow:rgba(155,123,255,.18)">
        <div class="num">04</div>
        <div class="kicker">CALIFORNIA · TECH POLICY</div>
        <h2 class="headline">CALIFORNIA · Bonta sues OpenAI</h2>
        <p class="detail">Model security, public safety</p>
      </article>

      <article class="card" style="--accent:#35d2b0;--glow:rgba(53,210,176,.18)">
        <div class="num">05</div>
        <div class="kicker">SOUTH KOREA · EDUCATION</div>
        <h2 class="headline">SOUTH KOREA · Choi Kyo-jin quits</h2>
        <p class="detail">Anti-AI rules disrupted exam</p>
      </article>

      <article class="card" style="--accent:#6fd36a;--glow:rgba(111,211,106,.18)">
        <div class="num">06</div>
        <div class="kicker">COP31 · ANTALYA</div>
        <h2 class="headline">COP31 ANTALYA · UN climate talks end</h2>
        <p class="detail">No deal; extreme weather worsens</p>
      </article>
    </section>

    <footer class="footer">
      <span><span class="mark">●</span> NEWS / WORLD / 23 NOV 2026</span>
      <span>FROM THE DAY'S WIRES</span>
    </footer>
  </main>
</body>
</html>
"""


def chromium_binary() -> Path:
    for candidate in (Path("/usr/bin/chromium"), Path("/snap/bin/chromium")):
        if candidate.is_file():
            return candidate
    raise SystemExit("No local Chromium binary found")


GUIDE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>make.fun entry guide · news-image-20261123</title>
<style>
  * { box-sizing: border-box; }
  html, body { width: 1200px; height: 1700px; margin: 0; overflow: hidden; }
  body {
    font-family: "DejaVu Sans", Arial, sans-serif;
    color: #eef3ff;
    background:
      radial-gradient(circle at 88% 0%, rgba(105,80,220,.30), transparent 34%),
      radial-gradient(circle at 0% 100%, rgba(20,120,150,.22), transparent 36%),
      linear-gradient(165deg, #101a31 0%, #080d1a 60%, #050810 100%);
  }
  .page { position: relative; width: 1200px; height: 1700px; padding: 70px 78px 60px; }
  .brand { display: flex; align-items: center; gap: 20px; }
  .logo {
    width: 78px; height: 78px; border-radius: 22px;
    background: linear-gradient(135deg, #7b5cff, #22c7a8);
    display: flex; align-items: center; justify-content: center;
    font-size: 46px; font-weight: 800; letter-spacing: -4px; color: #fff;
    box-shadow: 0 16px 40px rgba(70,60,190,.38);
  }
  .brand-name { font-size: 56px; font-weight: 800; letter-spacing: -2px; }
  .brand-name span { color: #7fe4cf; }
  .brand-sub { margin-top: 6px; font-size: 20px; letter-spacing: 5px; color: #91a5cb; font-weight: 700; }
  .hero { margin-top: 52px; }
  .eyebrow { font-size: 21px; font-weight: 800; letter-spacing: 4px; color: #8fa8d2; }
  h1 { margin: 18px 0 14px; font-size: 68px; line-height: 1.02; letter-spacing: -2.6px; }
  h1 em { color: #ffb85c; font-style: normal; }
  .lede { max-width: 1010px; font-size: 27px; line-height: 1.42; color: #cbd7ee; }
  .badges { margin-top: 34px; display: flex; gap: 16px; flex-wrap: wrap; }
  .badge {
    min-width: 250px; height: 62px; padding: 10px 18px;
    border: 1px solid rgba(180,200,240,.22); border-radius: 14px;
    background: rgba(255,255,255,.04);
    display: flex; align-items: center; gap: 12px;
    font-size: 19px; font-weight: 700; color: #c8d7f2;
  }
  .badge img { height: 34px; max-width: 150px; }
  .main { margin-top: 48px; display: grid; grid-template-columns: 520px 1fr; gap: 46px; align-items: start; }
  .preview {
    border: 1px solid rgba(180,200,240,.24); border-radius: 22px; padding: 16px;
    background: rgba(255,255,255,.035);
    box-shadow: 0 22px 60px rgba(0,0,0,.34);
  }
  .preview img { display: block; width: 488px; height: 488px; border-radius: 12px; }
  .preview-cap { margin-top: 14px; text-align: center; font-size: 17px; letter-spacing: 2px; color: #8fa3c8; font-weight: 700; }
  .steps { counter-reset: step; }
  .step { position: relative; padding: 0 0 30px 76px; }
  .step::before {
    counter-increment: step; content: counter(step);
    position: absolute; left: 0; top: 0;
    width: 50px; height: 50px; border-radius: 14px;
    background: rgba(127,228,207,.12); border: 1px solid rgba(127,228,207,.38);
    color: #7fe4cf; font-size: 25px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
  }
  .step h2 { margin: 4px 0 8px; font-size: 31px; letter-spacing: -.6px; }
  .step p { margin: 0; font-size: 23px; line-height: 1.4; color: #c4d0e8; }
  .panel {
    margin-top: 26px; padding: 26px 30px; border-radius: 20px;
    border: 1px solid rgba(123,92,255,.35);
    background: linear-gradient(135deg, rgba(123,92,255,.13), rgba(34,199,168,.09));
  }
  .panel-label { font-size: 18px; font-weight: 800; letter-spacing: 3px; color: #9fb6e0; }
  .link {
    display: block; margin-top: 12px; font-size: 23px; line-height: 1.35;
    color: #8ff0d8; word-break: break-all; text-decoration: none;
  }
  .foot {
    position: absolute; left: 78px; right: 78px; bottom: 42px;
    padding-top: 20px; border-top: 1px solid rgba(180,200,240,.16);
    display: flex; justify-content: space-between;
    font-size: 17px; letter-spacing: 2px; color: #7186aa; font-weight: 700;
  }
</style>
</head>
<body>
  <main class="page">
    <div class="brand">
      <div class="logo">m.</div>
      <div>
        <div class="brand-name">make<span>.fun</span></div>
        <div class="brand-sub">ENTRY GUIDE</div>
      </div>
    </div>

    <section class="hero">
      <div class="eyebrow">NEWS-IMAGE-20261123 · GITHUB ENTRY</div>
      <h1>An AI agent built this <em>world news image</em></h1>
      <p class="lede">A single 1024×1024 editorial graphic summarizes six verified stories from Monday 23 November 2026, with large type, regional breadth and a clean dark front-page layout.</p>
      <div class="badges">
__BADGES__
      </div>
    </section>

    <section class="main">
      <div class="preview">
        <img src="__ENTRY_URI__" alt="Submitted news infographic">
        <div class="preview-cap">ENTRY.PNG · 1024×1024</div>
      </div>

      <div class="steps">
        <div class="step">
          <h2>Brief</h2>
          <p>Six short, faithful cards cover Ukraine, Indonesia, US markets, California, South Korea and COP31 in Antalya.</p>
        </div>
        <div class="step">
          <h2>Artwork</h2>
          <p>Original HTML, CSS and SVG only: a hand-built grid, accent bars and a faint vector globe. No photos or copied artwork.</p>
        </div>
        <div class="step">
          <h2>Render</h2>
          <p>The offline renderer drives headless Chromium at fixed size, producing the deterministic PNG submitted for the bounty.</p>
        </div>

        <div class="panel">
          <div class="panel-label">OPEN THIS ENTRY</div>
          <a class="link" href="__LINK__">__LINK__</a>
        </div>
      </div>
    </section>

    <div class="foot">
      <span>MAKE.FUN · BUILT BY AN AI AGENT</span>
      <span>23 NOVEMBER 2026</span>
    </div>
  </main>
</body>
</html>
"""


def guide_page() -> str:
    payload = json.loads(REFERRAL_JSON.read_text(encoding="utf-8"))
    link = payload["link"]
    if not isinstance(link, str) or not link:
        raise SystemExit("Referral link missing from local data")

    badge_markup = "\n".join(
        f'      <div class="badge"><img src="{src}" alt="{html_lib.escape(label)}" '
        f'onerror="this.style.display=\'none\'"><span>{html_lib.escape(label)}</span></div>'
        for label, src in BADGES
    )
    safe_link = html_lib.escape(link, quote=True)
    return (
        GUIDE_TEMPLATE
        .replace("__BADGES__", badge_markup)
        .replace("__ENTRY_URI__", (ROOT / "entry.png").as_uri())
        .replace("__LINK__", safe_link)
    )


def render_entry() -> None:
    output = ROOT / "entry.png"
    browser = chromium_binary()

    # The snap Chromium sandbox has a private /tmp, so keep the source page
    # beside the script where the browser can always read it.
    with tempfile.TemporaryDirectory(prefix=".build-", dir=ROOT) as tmp:
        tmp_path = Path(tmp)
        html_path = tmp_path / "page.html"
        html_path.write_text(HTML, encoding="utf-8")

        command = [
            str(browser),
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--headless=new",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--screenshot={output}",
            "--force-device-scale-factor=1",
            "--force-color-profile=srgb",
            "--disable-background-networking",
            "--disable-extensions",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-dev-shm-usage",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=1200",
            f"--user-data-dir={tmp_path / 'profile'}",
            html_path.as_uri(),
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_guide() -> None:
    GUIDE_HTML.write_text(guide_page(), encoding="utf-8")
    command = [
        str(chromium_binary()),
        "--headless",
        "--no-sandbox",
        "--force-device-scale-factor=1",
        f"--window-size={GUIDE_WIDTH},{GUIDE_HEIGHT}",
        f"--screenshot={ROOT / 'screenshot.png'}",
        GUIDE_HTML.as_uri(),
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render() -> None:
    render_entry()
    render_guide()


if __name__ == "__main__":
    render()

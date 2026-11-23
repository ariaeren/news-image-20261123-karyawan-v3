#!/usr/bin/env python3
"""Render the 1024x1024 news infographic and its preview with headless Chromium."""

from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
WIDTH = 1024
HEIGHT = 1024

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


def render() -> None:
    output = ROOT / "entry.png"
    preview = ROOT / "screenshot.png"
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

    shutil.copyfile(output, preview)


if __name__ == "__main__":
    render()

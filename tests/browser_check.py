#!/usr/bin/env python3
"""Chromium smoke tests: 4 viewports, diagrams, equations, interaction, print.

Run after: python -m pip install playwright
           python -m playwright install --with-deps chromium
"""
from __future__ import annotations
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "browser"
OUT.mkdir(parents=True, exist_ok=True)
PAGES = ["index.html"] + [f"lessons/{i:02d}.html" for i in range(1,9)]
VIEWS = [(1440,900), (768,1024), (390,844), (360,800)]
errors=[]
measurements=[]

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for path in PAGES:
        for width,height in VIEWS:
            page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
            js_errors=[]
            page.on("pageerror",lambda exception: js_errors.append(str(exception)))
            page.on("console",lambda msg: js_errors.append("console: "+msg.text) if msg.type=="error" else None)
            page.goto((ROOT/path).as_uri(),wait_until="load")
            page.wait_for_timeout(150)
            label=Path(path).stem
            stats=page.evaluate("""() => ({
              viewport: window.innerWidth,
              scroll: document.documentElement.scrollWidth,
              h1: document.querySelectorAll('h1').length,
              main: !!document.querySelector('main')
            })""")
            if stats["scroll"]>stats["viewport"]+1:
                errors.append(f"{path} {width}px horizontal overflow: {stats['scroll']}")
            if stats["h1"]!=1 or not stats["main"]:
                errors.append(f"{path} {width}px invalid main/h1: {stats}")
            for image in page.locator("img").all():
                image.scroll_into_view_if_needed()
                try:
                    image.evaluate("(el) => el.decode()")
                    if not image.evaluate("(el) => el.complete && el.naturalWidth > 0"):
                        errors.append(f"{path} {width}px image has no natural width: {image.get_attribute('src')}")
                except Exception as ex:
                    errors.append(f"{path} {width}px image decode failed: {image.get_attribute('src')}: {ex}")
            if path.startswith("lessons/"):
                if page.locator("nav[aria-label]").count()==0:
                    errors.append(f"{path}: no navigation")
                if path.endswith(("02.html","03.html","07.html","08.html")):
                    count=page.locator("math").count()
                    if count==0: errors.append(f"{path}: MathML missing")
                    for expression in page.locator("math").all():
                        if expression.evaluate("(el) => el.getBoundingClientRect().height")<=0:
                            errors.append(f"{path}: MathML zero geometry")
                if path.endswith("01.html"):
                    page.locator('[data-demo="choice"] select').select_option("lookup")
                    if "哈希表" not in page.locator('[data-demo="choice"] output').inner_text():
                        errors.append("choice demo failed")
                elif path.endswith("02.html"):
                    page.locator('#growth-n').evaluate("""el => {el.value='32';el.dispatchEvent(new Event('input',{bubbles:true}));}""")
                    if "n = 32" not in page.locator('[data-demo="growth"] output').inner_text():
                        errors.append("growth demo failed")
                elif path.endswith("03.html"):
                    page.locator('#range-l').evaluate("""el => {el.value='2';el.dispatchEvent(new Event('input',{bubbles:true}));}""")
                    page.locator('#range-r').evaluate("""el => {el.value='5';el.dispatchEvent(new Event('input',{bubbles:true}));}""")
                    if "= 5。" not in page.locator('[data-demo="range"] output').inner_text():
                        errors.append("prefix interactive demo failed")
                elif path.endswith("04.html"):
                    page.locator("#reverse-step").evaluate("""el => {el.value='3';el.dispatchEvent(new Event('input',{bubbles:true}));}""")
                    if "反转结束" not in page.locator('[data-demo="reverse-links"] output').inner_text():
                        errors.append("linked-list reversal trace failed")
                elif path.endswith("05.html"):
                    page.locator("#bracket-step").evaluate("""el => {el.value='6';el.dispatchEvent(new Event('input',{bubbles:true}));}""")
                    if "栈自底向顶：空" not in page.locator('[data-demo="bracket-trace"] output').inner_text():
                        errors.append("bracket trace failed")
                elif path.endswith("06.html"):
                    page.locator("#ring-step").evaluate("""el => {el.value='6';el.dispatchEvent(new Event('input',{bubbles:true}));}""")
                    if "size=4" not in page.locator('[data-demo="ring-queue"] output').inner_text():
                        errors.append("circular queue trace failed")
                elif path.endswith("07.html"):
                    page.locator("#hash-key").select_option("17")
                    if "桶 2" not in page.locator('[data-demo="hash-bucket"] output').inner_text():
                        errors.append("hash bucket demo failed")
                elif path.endswith("08.html"):
                    page.locator("#tree-mode").select_option("level")
                    if "4 → 2 → 6" not in page.locator('[data-demo="tree-traversal"] output').inner_text():
                        errors.append("tree traversal demo failed")
            else:
                if page.locator('.chapter-card').count()!=28:
                    errors.append("homepage chapter cards != 28")
                page.locator("#chapter-search").fill("动态规划")
                if page.locator('.chapter-card:visible').count()!=1:
                    errors.append("homepage filter failed")
                page.locator("#chapter-search").fill("")
            if js_errors:
                errors.extend(f"{path} {width}px {msg}" for msg in js_errors)
            page.screenshot(path=str(OUT/f"{label}-{width}.png"),full_page=True,animations="disabled")
            measurements.append({"page":path,"width":width,"height":height,"overflow":stats["scroll"]-stats["viewport"],"js_errors":len(js_errors)})
            page.close()
    for number in (3, 8):
        print_page=browser.new_page(viewport={"width":960,"height":900})
        print_page.goto((ROOT/f"lessons/{number:02d}.html").as_uri())
        print_page.emulate_media(media="print")
        if print_page.locator("article").evaluate("(el) => el.getBoundingClientRect().width")<200:
            errors.append(f"chapter {number}: print article has no width")
        print_page.screenshot(path=str(OUT/f"{number:02d}-print.png"),full_page=True)
        print_page.close()
    no_js=browser.new_page(java_script_enabled=False)
    no_js.goto((ROOT/"index.html").as_uri())
    if no_js.locator(".chapter-card").count()!=28:
        errors.append("homepage links depend on JavaScript")
    no_js.goto((ROOT/"lessons/08.html").as_uri())
    if no_js.locator("figure").count()<2:
        errors.append("chapter 08 diagrams depend on JavaScript")
    no_js.close()
    browser.close()
report={"checks":measurements,"errors":errors}
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
if errors:
    print("\n".join("FAIL "+error for error in errors))
    raise SystemExit(1)
print("OK:",len(measurements),"viewport checks, print, images, demos and MathML geometry")

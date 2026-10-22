from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent/'top_restored'
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1200})
    page.goto((root/'index.html').as_uri())
    page.screenshot(path=str(root/'トップページ再現_冒頭.png'))
    page.screenshot(path=str(root/'トップページ再現_PC.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(root/'トップページ再現_スマホ.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.evaluate('[...document.images].every(x => !x.src.startsWith("http"))')
    print('PC/mobile width and local image checks passed')
    browser.close()

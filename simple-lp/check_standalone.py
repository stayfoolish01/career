from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(offline=True,viewport={'width':390,'height':844})
    page=context.new_page()
    errors=[]
    requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto((root/'スタディングキャリア_共有用.html').as_uri())
    assert page.locator('.job-card').count()==6
    page.locator('[data-filter="簿記"]').click()
    assert page.locator('.job-card').count()==2
    page.locator('.card-detail').first.click()
    page.locator('#job-register').click()
    assert page.locator('#selected-job').is_visible()
    page.locator('#name').fill('Test User')
    page.locator('#email').fill('test@example.com')
    page.locator('input[name="qualification"]').first.check()
    page.locator('#consent').check()
    page.locator('#registration [type="submit"]').click()
    assert page.locator('#confirmation').evaluate('(x)=>x.open')
    page.locator('#finish-demo').click()
    assert page.locator('#name').input_value()==''
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.evaluate('[...document.images].every(x=>x.complete && x.naturalWidth>0)')
    assert not errors,errors
    assert not [u for u in requests if u.startswith(('https:','http:'))],requests
    browser.close()
    print('PASS: offline file, embedded images, filter/detail, registration preview/reset, mobile, no HTTP requests or JS errors')

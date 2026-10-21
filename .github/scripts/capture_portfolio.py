"""Capture actual rendered pages and exercise browser navigation in GitHub Actions."""
from pathlib import Path
import re
import time
import urllib.request
from playwright.sync_api import sync_playwright

for attempt in range(60):
    try:
        urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=2)
        break
    except Exception:
        time.sleep(1)
else:
    raise RuntimeError('Streamlit did not start')

output = Path('docs/screenshots')
output.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width':1600,'height':1200}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://localhost:8501', wait_until='domcontentloaded')

    def capture(filename, charts=True):
        page.get_by_test_id('stAppViewContainer').wait_for()
        # Streamlit renders asynchronously over WebSockets; allow the page run to finish.
        page.wait_for_timeout(5000)
        if page.get_by_test_id('stException').count():
            raise RuntimeError(page.get_by_test_id('stException').all_text_contents())
        if charts and not page.get_by_test_id('stPlotlyChart').count():
            raise RuntimeError('Expected chart did not render')
        page.screenshot(path=str(output / filename), full_page=False)

    page.get_by_text('Network command centre', exact=True).wait_for()
    page.wait_for_timeout(2500)
    if not page.evaluate("document.fonts.ready.then(() => document.fonts.check('14px Inter'))"):
        raise RuntimeError('Bundled Inter font did not load')
    if page.locator('.metric-tile').count() != 6:
        raise RuntimeError('Expected six consistent headline cards')
    label_size = page.locator('.metric-tile-label').first.evaluate('(el) => parseFloat(getComputedStyle(el).fontSize)')
    if label_size < 12:
        raise RuntimeError('Metric labels are too small')
    if page.locator('img.metric-spark').count() != 6:
        raise RuntimeError('Source-data sparklines did not render')
    broken = page.locator('.metric-grid img').evaluate_all('(images) => images.some(img => !img.complete || img.naturalWidth === 0)')
    if broken:
        raise RuntimeError('Card image failed to load')
    capture('overview.png')
    page.get_by_role('tab', name='Investigation queue', exact=True).click()
    capture('investigation-queue.png')
    page.get_by_test_id('stSidebar').get_by_text('Technology intelligence', exact=False).click()
    page.get_by_role('button', name='4G performance', exact=True).click()
    capture('technology-4g.png')
    page.get_by_role('button', name=re.compile('Site analytics')).click()
    capture('site-analytics.png')
    page.get_by_role('button', name=re.compile('Project case study')).click()
    capture('project-case-study.png', charts=False)
    page.get_by_role('button', name='Explore the command centre', exact=True).click()
    page.wait_for_timeout(4000)
    page.set_viewport_size({'width':390,'height':844})
    collapse = page.get_by_test_id('stSidebarCollapseButton')
    if collapse.count() and collapse.is_visible():
        collapse.click()
    capture('overview-mobile.png')
    if page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 2'):
        raise RuntimeError('Page-level horizontal overflow on mobile')
    if errors:
        raise RuntimeError(errors)
    browser.close()

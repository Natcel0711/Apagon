import asyncio
from playwright.async_api import async_playwright
import json
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 3440, "height": 1440})
        await page.goto("https://miluma.lumapr.com/outages/outageMap")
        for e in range(3):
            await page.locator("[aria-label='Zoom out']").click()
            await page.wait_for_timeout(1000)
        rows = page.locator('.jss56')
        count = await rows.count()
        for i in range(count):
            await rows.nth(i).click()
            await page.locator('.jss72').click()
            Pueblo = await page.inner_text('.MuiAccordionSummary-content')
            detalles = await page.inner_text('.MuiAccordionDetails-root')
            sectores = detalles.split("\n")
            while("" in sectores):
                sectores.remove("")
            Cantidad = sectores.pop(0)
            dic = {
                "Pueblo":Pueblo.split('-')[1],
                "Cantidad":Cantidad,
                "Sectores":sectores
            }
            res = json.dumps(dic, sort_keys=True, indent=4)
            print(res)
        await browser.close()

asyncio.run(main())
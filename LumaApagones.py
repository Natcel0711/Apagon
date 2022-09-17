import asyncio
from playwright.async_api import async_playwright
import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
my_url = os.getenv("SUPABASE_URL")
my_key = os.getenv("SUPABASE_KEY")

async def Select():
    url: str = my_url
    key: str = my_key
    supabase: Client = create_client(url, key)
    data = supabase.table("Apagon").select("JsonData").execute()
    # Assert we pulled real data.
    assert len(data.data) > 0
    DataJSON = data.data[0]
    print(DataJSON.get('JsonData'))

async def main():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            dicks = []
            await page.set_viewport_size({"width": 3440, "height": 1440})
            await page.goto("https://miluma.lumapr.com/outages/outageMap")
            for e in range(3):
                await page.locator("[aria-label='Zoom out']").click()
                await page.wait_for_timeout(1000)
            rows = page.locator('.jss56')
            count = await rows.count()
            added = []
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
                    "Pueblo":Pueblo.split('-')[1].strip(),
                    "Cantidad":Cantidad,
                    "Sectores":sectores
                }
                if dic['Pueblo'] in added:
                    print(f"{dic['Pueblo']} already in list")
                else:
                    dicks.append(dic)
                    added.append(dic["Pueblo"])  
            res = json.dumps(dicks, indent=2)
            print(res)
            url: str = my_url
            key: str = my_key
            supabase: Client = create_client(url, key)
            data = supabase.table("Apagon").update({"JsonData":res}).eq('id', 34).execute()
            assert len(data.data) > 0    
            await browser.close()
    except:
        print("Error")
asyncio.run(main())

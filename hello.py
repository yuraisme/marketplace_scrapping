import asyncio
import json
import os
import random
import time

from dotenv import load_dotenv
from fake_useragent import UserAgent
from playwright.async_api import TimeoutError, async_playwright

WIDTH = [1240, 1002, 1801, 1443, 1327]
HEIGHT = [711, 633, 855, 715, 901, 693]
PROXY = [None]
load_dotenv()

if os.getenv("PROXY_PLAY"):
    PROXY += json.loads(os.getenv("PROXY_PLAY") or "{}")


async def load_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=True,
            proxy=random.choice(PROXY),
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )
        context = await browser.new_context(
            user_agent=UserAgent().random,
            viewport={
                "width": random.choice(WIDTH),
                "height": random.choice(HEIGHT),
            },
            locale="ru-RU",
            timezone_id="Europe/Moscow",
        )
        page = await context.new_page()

        try:
            await page.add_init_script(path="playwright-stealth.js")
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_selector(
                "div.price-block__content:visible", timeout=60000
            )
            price_element = await page.query_selector(
                "div.price-block__content:visible"
            )
            if price_element:
                text = await price_element.inner_text()
                await browser.close()
                return text.split("\n")[0]
            else:
                print(f"Элемент не найден для {url}")
                await browser.close()
                return None
        except TimeoutError:
            await page.screenshot(path=f"error_{int(time.time())}.png")
            print(f"Таймаут для {url}, скриншот сохранён")
            await browser.close()
            return None


async def main(urls: list[str]):
    PARALLEL_LOADS = 4
    count_pages = 0
    random.shuffle(urls)
    while count_pages < len(urls):
        urls_chunk = urls[
            count_pages : min(count_pages + PARALLEL_LOADS, len(urls))
        ]
        tasks = [load_page(url.strip()) for url in urls_chunk]
        res = await asyncio.gather(*tasks)
        print(f"{count_pages}| {res} /: {time.strftime('%H:%M:%S')}")
        count_pages += PARALLEL_LOADS


if __name__ == "__main__":

    with open("urls.txt", "r") as url_file:
        urls = url_file.readlines()
        print("Файл загружен")
        print(time.strftime("%H:%M:%S"))
    asyncio.run(main(urls))

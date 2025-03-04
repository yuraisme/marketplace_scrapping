import json
import os
import random

from dotenv import load_dotenv
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright

WIDTH = [1240, 1002, 1801, 1443, 1327]
HEIGHT = [711, 633, 855, 715, 901, 693]
load_dotenv()
proxy = json.loads(os.getenv("PROXY_PLAY") or "")

def extract_product_links(url):
    # Запускаем Playwright
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            proxy=random.choice(proxy),
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )
        context = browser.new_context(
            user_agent=UserAgent().random,
            viewport={
                "width": random.choice(WIDTH),
                "height": random.choice(HEIGHT),
            },
            locale="ru-RU",
            timezone_id="Europe/Moscow",
        )
        page = context.new_page()
        page.add_init_script(path="playwright-stealth.js")

        # page.goto(url)
        page.goto(url, wait_until="domcontentloaded")
        # Ждем, пока загрузятся карточки продуктов
        page.wait_for_selector(".k8j_24")

        # Находим все карточки продуктов
        product_cards = page.query_selector_all(".k8j_24")

        # Список для хранения ссылок
        product_links = []
        print(product_cards)
        # Проходим по каждой карточке
        for card in product_cards:
            # Находим элемент ссылки внутри карточки
            link_element = card.query_selector(".k8j_24")
            if link_element:
                # Извлекаем атрибут href
                href = link_element.get_attribute("href")
                if href:
                    product_links.append(href)

        # Закрываем браузер
        browser.close()
        # Возвращаем список ссылок
        return product_links


# Пример использования
for i in range(1, 2):
    url = "https://www.ozon.ru/product/kurtka-boos-jack-demisezonnaya-1857774908/?at=x6tPjz9rrHYJOrKVTxDvz0RfrRqwr7szN1O6OCRxGEno"
    links = extract_product_links(url)
    for link in links:
        print(link)

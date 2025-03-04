import json
import os
import random
import time

from dotenv import load_dotenv
from DrissionPage import Chromium, ChromiumPage
from DrissionPage.common import ChromiumOptions, Settings
from DrissionPage.errors import BrowserConnectError, ElementNotFoundError

load_dotenv()
PROXIES = []
if os.getenv("PROXY_PLAY"):
    PROXIES += json.loads(os.getenv("PROXY_DRIS") or "{}")


def kill_chromium_processes():
    if os.name == "nt":  # Windows
        os.system("taskkill /im chrome.exe /f")
    else:  # Linux/Mac
        os.system("pkill -9 chrome")


def parse_ozon(url):
    # time.sleep(random.randrange(1, 3))
    # kill_chromium_processes()
    Settings.set_language("en")
    Settings.set_raise_when_wait_failed(True)
    Settings.set_raise_when_ele_not_found(True)
    co = ChromiumOptions().set_browser_path(r"chromium\bin\chrome.exe")
    co.no_imgs(True).headless(True)

    if random.choice([True, False]):
        # print('Whith proxy')
        co.set_proxy(random.choice(PROXIES))
    # co.incognito(True)

    co.set_user_agent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    )
    tab = Chromium(co).latest_tab
    # tab = ChromiumPage(addr_or_opts=co)
    try:
        if not isinstance(tab,str):
            if tab.get(url):

                tab.get_screenshot(path="screenshot.png")
                p = tab.ele(".l1w_28 lw_28")
                # print(f'{price.text}   {time.strftime("%H:%M:%S")}')
                # tab.close()
                os.remove("screenshot.png")
                if p:
                    return p.text
        else:
            raise BrowserConnectError()
    except ElementNotFoundError:
        print("Товар не найден")
        print(url)
    except Exception as e:
        print(e)
        print(url)

    # tab.close()


if __name__ == "__main__":
    with open("urls_ozon.txt", "r") as file:
        urls = file.readlines()
    if urls:
        print(time.strftime("%H:%M"))
        for key, url in enumerate(urls):
            price = parse_ozon(url)
            if price:
                print(
                    f'{key}.  {price.replace(' ','')}   {time.strftime("%H:%M:%S")}'
                )
    kill_chromium_processes()

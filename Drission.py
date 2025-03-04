import time

from DrissionPage import Chromium, ChromiumPage
from DrissionPage.common import ChromiumOptions, Settings

Settings.set_language("en")


co = ChromiumOptions()
co.no_imgs(True)

co.headless(True)
# co.incognito(True)
co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
# tab = Chromium(co).latest_tab
tab = ChromiumPage(addr_or_opts=co)

# page = SessionPage()
tab.get(
    "https://www.ozon.ru/category/smartfony-15502/"
    # "https://browserleaks.com/http2"
)
tab.wait(1)
for i in range(10):
    # tab.actions.scroll(delta_y=(1000))
    tab.scroll.down(1000)
    time.sleep(1)
tab.get_screenshot(path="screenshot.png")
links = tab.eles(".i6z_24 iz7_24 tile-root")
for link in links:
    with open('urls_ozon.txt','a') as file:
        print(link.ele("tag:a").link)    
        file.writelines([link.ele("tag:a").link,'\n'])    
print(len(links))
tab.quit()
# tab.close()

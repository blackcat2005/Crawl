import asyncio
import pyppeteer
import random
import string
import requests

# Import Detection From Stealth
from tiktok.stealth import stealth


class browser:

    def __init__(self, url, language='en', find_redirect=False):
        self.url = url
        self.referrer = "https://www.tiktok.com/"
        self.language = language

        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.0 Safari/537.36)"
        self.args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            "--window-position=0,0",
            "--ignore-certifcate-errors",
            "--ignore-certifcate-errors-spki-list",
             "--user-agent=" + self.userAgent
        ]

        self.options = {
            'args': self.args,
            'headless': True,
            'ignoreHTTPSErrors': True,
            'userDataDir': "./tmp",
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False
        }

        loop = asyncio.new_event_loop()

        if find_redirect:
            loop.run_until_complete(self.find_redirect())
        else:
            loop.run_until_complete(self.start())

    async def start(self):
        self.browser = await pyppeteer.launch(self.options)
        self.page = await self.browser.newPage()

        await self.page.evaluateOnNewDocument("""() => {
    delete navigator.__proto__.webdriver;
        }""")

        # might have to switch to a tiktok url if they improve security
        await self.page.goto("about:blank", {
            'waitUntil': "load"
        })

        self.userAgent = await self.page.evaluate("""() => {return navigator.userAgent; }""")

        self.verifyFp = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(16))

        await self.page.evaluate("() => { " + self.__get_js() + " }")

        self.signature = await self.page.evaluate('''() => {
        var url = "''' + self.url + "&verifyFp=" + self.verifyFp + '''"
        var token = window.byted_acrawler.sign({url: url});
        return token;
        }''')

        if self.url != None:
            await self.page.goto(self.url +
                                "&verifyFp=" + self.verifyFp +
                                "&_signature=" + self.signature, {
                                    'waitUntil': "load"
                                })

            self.data = await self.page.content()
            self.url += "&verifyFp=" + self.verifyFp + "&_signature=" + self.signature

        await self.browser.close()
        await self.browser.close()
        self.browser.process.communicate()

    async def find_redirect(self):
        try:
            self.browser = await pyppeteer.launch(self.options)
            self.page = await self.browser.newPage()

            await self.page.evaluateOnNewDocument("""() => {
        delete navigator.__proto__.webdriver;
    }""")

            # Check for user:pass proxy

            await stealth(self.page)
            await self.page.goto(self.url, {
                'waitUntil': "load"
            })

            self.redirect_url = self.page.url

            await self.browser.close()
            self.browser.process.communicate()

        except:
            await self.browser.close()
            self.browser.process.communicate()

    def __get_js(self):
        return requests.get("https://sf16-muse-va.ibytedtos.com/obj/rc-web-sdk-gcs/acrawler.js").text

if __name__ == '__main__':
    b = browser("https://m.tiktok.com/api/item_list/?count=30&id=1&type=5&secUid=&maxCursor=0&minCursor=0&sourceType=12&appId=1233&region=US&language=en")
    pass
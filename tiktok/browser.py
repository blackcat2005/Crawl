import asyncio
import pyppeteer as py
import string
import random


class browser:

    def __init__(self, url, lang='en'):
        self.url = url
        self.referrer = 'https://www.tiktok.com/'
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
        self.verifyFp = ''
        self.signature = ''

        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.main())

    async def main(self):
        b = await py.launch(self.options)
        page = await b.newPage()
        await page.evaluateOnNewDocument("""() => {
                            delete navigator.__proto__.webdriver;
                                }""")

        await page.goto("https://www.tiktok.com/foryou?lang=en", {'waitUntil': "load"})
        self.verifyFp = ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(16))
        print(self.verifyFp)
        self.signature = await page.evaluate('''() => {
                            var url = "''' + self.url + "&verifyFp=" + self.verifyFp + '''"
                            var token = window.byted_acrawler.sign({url: url});
                            return token;
                            }''')
        print(self.signature)

        await page.goto(self.url + "&verifyFp=" + self.verifyFp + "&_signature=" + self.signature, {'waitUntil': "load"})
        data = await page.content()
        if data != None:
            self.url += "&verifyFp=" + self.verifyFp + "&_signature=" + self.signature
            pass

        await b.close()
        b.process.communicate()

if __name__ == '__main__':
    pass

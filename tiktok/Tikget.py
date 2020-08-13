import re
import requests as req
import json
from functools import wraps
from tiktok.browser import browser
from bs4 import BeautifulSoup as html


class Tikget:
    
    class _Decorator:
        @classmethod
        def countDef(cls, func):
            """
            Decorator for function having parameter count
            :param func
            :return:
            """

            @wraps(func)
            # count here is really work
            def wrap_func(self, *args, count=10, **kwargs):
                response = []
                maxCount = 50
                maxCursor = 0
                first = True

                while len(response) < count:
                    realCount = count if count < maxCount else maxCount
                    res = func(self, *args, realCount, **kwargs, maxCursor=maxCursor)

                    try:
                        res['items']
                    except:
                        print("Most Likely User's List is Empty")
                        return []

                    if 'items' in res.keys():
                        for t in res['items']:
                            response.append(t)

                    if not res['hasMore'] and not first:
                        print("TikTok isn't sending more TikToks beyond this point.")
                        return response

                    realCount = count - len(response)
                    maxCursor = res['maxCursor']

                    first = False

                return response[:count]

            return wrap_func

    def __init__(self):
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95 '

    def data(self, api_url):
        """
        Return data from api
        :param api_url:
        :param language:
        :return: json
        """
        b = browser(api_url)
        #api_url += f"&verifyFp={b.verifyFp}&_signature={b.signature}"
        header = {
            'authority': 'm.tiktok.com',
            "method": "GET",
            'path': api_url.split("tiktok.com")[1],
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            "accept-encoding": "utf-8",
            'accept-language': 'en-US,en;q=0.9',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            "user-agent": b.userAgent
        }
        r = req.get(b.url, headers=header)

        try:
            # print(b.url)
            return r.json()
        except:
            print("Convert error")

    def bytes(self, api_url):
        """
        return bytes to download
        :param api_url:
        :param language:
        :return: iter_content()
        """

        b = browser(api_url)
        header = {
            'authority': 'm.tiktok.com',
            "method": "GET",
            'path': api_url.split("tiktok.com")[1],
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            "accept-encoding": "utf-8",
            'accept-language': 'en-US,en;q=0.9',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            "user-agent": b.userAgent
        }
        r = req.get(b.url, headers=header)
        return r.iter_content(chunk_size=128)

    @_Decorator.countDef
    def trending(self, count=0, language='en', region='US', maxCursor=0):
        """
        Get trending
        :param maxCursor:
        :param count:
        :param language:
        :param region:
        :return:
        """
        api_url = f"https://m.tiktok.com/api/item_list/?count={count}&id=1&type=5&secUid=&maxCursor={maxCursor}&minCursor=0&sourceType=12&appId=1233&region={region}&language={language}"
        return self.data(api_url)

    def user(self, username, language='en'):
        """
        Get User information from uniqueID (username)
        :param username:
        :param language:
        :return:
        """
        api_url = f'https://m.tiktok.com/api/user/detail/?uniqueId={username}&language={language}'
        return self.data(api_url)

    @_Decorator.countDef
    #count here is fake
    def postsUser(self, userID, secUID, count=0, language='en', region='US', maxCursor=0):
        """
        Get user'sPost from userID, secUID
        :param userID:
        :param secUID:
        :param count:
        :param language:
        :param region:
        :return: list
        """
        api_url = f"https://tiktok.com/api/item_list/?count={count}&id={userID}&type=1&secUid={secUID}&maxCursor={maxCursor}&minCursor=0&sourceType=8&appId=1233&region={region}&language={language}"
        return self.data(api_url)

    def postsByName(self, username, count=10, language='en', region='US'):
        """
          Gets a specific user's tiktoks by username
        """
        data = self.user(username)['userInfo']['user']
        return self.postsUser(data['id'], data['secUid'], count=count, language=language, region=region)

    @_Decorator.countDef
    def likedUser(self, userID, secUID, count=0, language='en', region='US', maxCursor=0):
        """
        Get a user's liked posts
        :param userID:
        :param secUID:
        :param count:
        :param language:
        :param region:
        :param maxCursor:
        :return:
        """
        api_url = f"https://m.tiktok.com/api/item_list/?count={count}&id={userID}&type=2&secUid={secUID}&maxCursor={maxCursor}&minCursor=0&sourceType=9&appId=1233&region={region}&language={language}&verifyFp= "
        return self.data(api_url)
    
    def itemsByID(self, id, language='en'):
        """
        Get a tiktok object by id
        :param id:
        :param language:
        :return:
        """
        api_url = f"https://m.tiktok.com/api/item/detail/?itemId={id}&language={language}"
        return self.data(api_url)
        pass

    def itemsByUrl(self, url, language='en'):
        if "@" in url and "/video/" in url:
            post_id = url.split("/video/")[1].split("?")[0]
        else:
            raise Exception(
                 "URL format not supported. Below is an example of a supported "
                 "url.\nhttps://www.tiktok.com/@therock/video/6829267836783971589")
        return self.itemsByID(post_id, language)
        pass

    def music(self, url):
        data = self.itemsByUrl(url)
        return data["itemInfo"]["itemStruct"]["music"]["playUrl"]
    #sol1
    def videoNo(self, url):
        """
        Get video no watermark through tikmate
        :param url:
        :return:
        """
        api_url = url.replace(r'www.tiktok.com/@', 'www.tikmate.online/').replace('/video/', '/')
        if '?lang=vi' in api_url :
            api_url = api_url.replace('?lang=vi', '')
        head = {
            'authority': 'tikmate.online',
            'method': 'GET',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'utf-8',
            'referer': 'https://tikmate.online/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.userAgent
        }
        res = str(req.get(api_url, headers=head).content)
        pattern = re.compile(r'(source src=".*vr=")')
        try:
            link = pattern.search(res).group(0).replace(r'source src="', '').replace(r'"', '')
            return link
        except:
            return None

    def videoWT(self, url):
        """
        Get video with watermark by api
        :param url:
        :return:
        """
        # r = req.get(url, headers={"method": "GET",
        #                                      "accept-encoding": "utf-8",
        #                                      "user-agent": self.userAgent})
        # data = r.text
        # print(data)
        # pattern = re.compile(r'("video":{"urls":\[".*vr=)')
        # link = pattern.search(data).group(0).replace(r'"video":{"urls":["', '')
        #
        # return link.encode('utf8').decode('unicode-escape')
        data = self.itemsByUrl(url)
        return data["itemInfo"]["itemStruct"]["video"]["downloadAddr"]
        pass

    #sol2 error
    def _video(self, url):
        """
        Get all video through ssstiktok
        :param url:
        :return:
        """
        # get token
        # head = {
        #     "Accept-Encoding": "utf8",
        #     "Accept-Language": "en-US,en;q= 0.9",
        #     # "Connection": "keep-alive",
        #     "Content-Length": "137",
        #     "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        #     "Host": "ssstiktok.io",
        #     # "HX-Active-Element": "submit",
        #     "HX-Current-URL": "https://ssstiktok.io/vi",
        #     "HX-Request": "true",
        #     "HX-Target": "target",
        #     "Origin": "https://ssstiktok.io",
        #     # "Sec-Fetch-Dest": "empty",
        #     # "Sec-Fetch-Mode": "cors",
        #     # "Sec-Fetch-Site": "same-origin",
        #     "User-Agent": self.userAgent
        # }
        # r = req.get("https://ssstiktok.io").text
        # token = html(r, 'html.parser').find_all(id='token')[0].get('value')
        # print(token)
        # api_url = 'https://ssstiktok.io/api/1/fetch'
        # data = {
        #     "id": url,
        #     "token": token,
        #     "locale": "vi"
        # }
        # r = req.request('POST', api_url, headers=head, data=data)
        # soup = html(r.text, 'html.parser')
        # print(soup)
        # # With href not contains http
        # try:
        #     links = [_.get('href') if 'http' in _.get('href') else 'https://ssstiktok.io' + _.get('href') for _ in
        #              soup.find_all('a')]
        #     link = {
        #         'no1': links[0],  # link ssstiktok no wt
        #         'no2': links[1],  # link api no wt
        #         'wt1': links[2],  # link ssstiktok wt
        #         'wt2': links[3]  # link api wt
        #     }
        #     return link
        # except Exception as err:
        #     print(err)
        #     print('Cannot')
        #     return None
        # pass
        head = {
            "Accept-Encoding": "utf8",
            "Accept-Language": "en-US,en;q=0.9",
            # "Content-Length": "203",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            'origin': 'https://snaptik.app',
            'referer': 'https://snaptik.app/vn',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95'
        }
        api_url = 'https://snaptik.app/action-v9.php'
        data = {
            'url': url
        }
        r = req.request('POST', api_url, headers=head, data=data)
        soup = html(r.text, 'html.parser')
        print(soup)

    @staticmethod
    def getFilename(url):
        """
        Get file name from url video or url music
        :param url:
        :return:
        """
        if 'video' in url:
            return str(url.split("/")[-1]).split('?')[0] + '.mp4'
        elif 'mp3' in url:
            return str(url.split("/")[-1])

if __name__ == '__main__':
    get = Tikget()
    # user = get.user("tra.dang.904")
    # #userPost = get.postsUser('62962882845', 'MS4wLjABAAAAaOgKYENcaNEcIPP1lio_ZUeSp_Gt9FdzhngYgquVD1Q')
    # userPost = get.postsByName('linhbarbie', 10)
    # #trend = get.trending()
    # liked = get.likedUser('62962882845', 'MS4wLjABAAAAaOgKYENcaNEcIPP1lio_ZUeSp_Gt9FdzhngYgquVD1Q', 5)
    # tiktokobject = get.itemsByID('6855179879650954497')
    #
    # with open('result.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(userPost, ensure_ascii=False))

    #print(get.video('https://www.tiktok.com/@thonguyen011192/video/6855179879650954497?lang=vi'))
    #print(get.music('https://www.tiktok.com/@thonguyen011192/video/6855179879650954497?lang=vi'))
    # print(get.video('https://www.tiktok.com/@gingaming06/video/6859567263150787842?lang=vi'))
    pass

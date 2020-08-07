import requests as req
import json
from functools import wraps

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

    def data(self, api_url, language='vi'):
        """
        Return data from api
        :param api_url:
        :param language:
        :return: json
        """
        b = browser(api_url)
        api_url += f"&verifyFp={b.verifyFp}&_signature={b.signature}"
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
        r = req.get(api_url, headers=header)

        try:
            print(api_url)
            return r.json()
        except:
            print("Convert error")

    def bytes(self, api_url, language='vi'):
        """
        return bytes to download
        :param api_url:
        :param language:
        :return: iter_content()
        """
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
            "user-agent": self.userAgent
        }
        r = req.get(api_url, headers=header)
        return r.iter_content(chunk_size=128)

    @_Decorator.countDef
    def trending(self, count=0, language='vi', region='US', maxCursor=0):
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

    def user(self, username, language='vi'):
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
    def postsUser(self, userID, secUID, count=0, language='vi', region='US', maxCursor=0):
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

    def postsByName(self, username, count=0, language='en', region='US'):
        """
          Gets a specific user's tiktoks by username
        """
        data = self.user(username)['userInfo']['user']
        return self.postsUser(data['id'], data['secUid'], count=count, language=language, region=region)

    @_Decorator.countDef
    def likedUser(self, userID, secUID, count=0, language='vi', region='US', maxCursor=0):
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
        api_url = f"https://m.tiktok.com/api/item_list/?count={count}&id={userID}&type=2&secUid={secUID}&maxCursor={maxCursor}&minCursor=0&sourceType=9&appId=1233&region={region}&language={language}&verifyFp="
        return self.data(api_url)


if __name__ == '__main__':
    get = Tikget()
    user = get.user("tra.dang.904")
    #userPost = get.postsUser('62962882845', 'MS4wLjABAAAAaOgKYENcaNEcIPP1lio_ZUeSp_Gt9FdzhngYgquVD1Q')
    #userPost = get.postsByName('tra.dang.904', 10)
    trend = get.trending()
    #liked = get.likedUser('62962882845', 'MS4wLjABAAAAaOgKYENcaNEcIPP1lio_ZUeSp_Gt9FdzhngYgquVD1Q', 5)

    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(str(json.dumps(trend)))
        pass
    pass

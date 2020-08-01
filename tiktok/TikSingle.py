import requests as req
import re
import time
import sys


class TikSingle():
    url_ori = ''
    url = ''
    _head = {
        'authority': 'tikmate.online',
        'method': 'GET',
        'path': '/kanmei0112/6855626996748143873',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': '__cfduid=d9a3e98fa13b476fcc3f5681561cd0d951596247728; _ga=GA1.2.1473589781.1596247721; _gid=GA1.2.1537394676.1596247721; ads=ok; PHPSESSID=e5c62de0fe7802a61337c5aee8f49e22; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; __atuvc=3%7C31; __atuvs=5f2534403c020ad7001; _gat=1',
        'referer': 'https://tikmate.online/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95'
    }

    def __init__(self, url):
        self.url_ori = url
        self.url = url.replace(r'www.tiktok.com/@', 'www.tikmate.online/').replace('?lang=vi', '').replace('/video/', '/')

    def get_link(self):
        _res = str(req.get(self.url, headers=self._head).content)
        _pattern = re.compile(r'(source src=".*vr=")')
        _link = _pattern.search(_res).group(0).replace(r'source src="', '').replace(r'"', '')
        return _link

    def get_file_name(self):
        return str(self.url.split("/")[-1])

    def download(self, path=None):
        r = req.get(self.get_link(), stream=True)

        start_time = time.time()
        with open(self.get_file_name() + ".mp4", 'wb') as f:
            count = 1
            block_size = 512
            try:
                total_size = int(r.headers.get('content-length'))
                print('file total size :', total_size)
            except TypeError:
                print('using dummy length !!!')
                total_size = 10000000

            for chunk in r.iter_content(chunk_size=block_size):

                if chunk:  # filter out keep-alive new chunks

                    duration = time.time() - start_time
                    progress_size = int(count * block_size)
                    if duration == 0:
                        duration = 0.1
                    speed = int(progress_size / (1024 * duration))
                    percent = int(count * block_size * 100 / total_size)
                    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                                     (percent, progress_size / (1024 * 1024), speed, duration))

                    f.write(chunk)
                    f.flush()
                    count += 1

    def download_light(self, path=None):
        file = req.get(self.get_link(), allow_redirects=True)
        with open(self.get_file_name() + ".mp4", mode="wb") as f:
            f.write(file.content)


if __name__ == '__main__':
    get = TikSingle('https://www.tiktok.com/@phu_soya8/video/6855905022002203905?lang=vi')
    link = get.get_link()
    print(link)
    get.download()
    pass

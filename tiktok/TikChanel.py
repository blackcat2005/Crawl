from tiktok.Tikget import Tikget
from DownloadEffect import DownloadEffect as down


# Down video and sound from a chanel
#
class TikChanel:
    @classmethod
    def _getListID(cls, username, count=10):
        """
        Get list video (id) from username, default 10, max 50
        :param username:
        :param count:
        :return:
        """
        a = Tikget()
        posts = a.postsByName(username, count)
        for item in posts:
            yield item['id']
    pass

    @classmethod
    def _getLinkVideoDownload(cls, username, WT=False ,count=10):
        a = Tikget()

        for item in cls._getListID(username, count):
            url = f'https://www.tiktok.com/@{username}/video/{item}'
            if not WT:
                yield a.videoNo(url)
            else:
                yield {
                    'no': a.videoNo(url),
                    'wt': a.videoWT(url)
                }

    @classmethod
    def getLinkSoundDownload(cls, username, count=10):
        a = Tikget()

        for item in cls._getListID(username, count):
            url = f'https://www.tiktok.com/@{username}/video/{item}'
            yield a.music(url)

    @classmethod
    def downChanel(cls, username, count, option):
        lis = cls._getListID(username, count)
        a = down()
        for item in lis:
            a.download()

if __name__ == '__main__':
    test = TikChanel()
    for _ in test.getLinkSoundDownload('meodubaiii', 10):
        print(_)

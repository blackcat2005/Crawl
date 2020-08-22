from TikTokGet.Tikget import Tikget
from DownloadEffect import DownloadEffect as down
import pathlib as pa
import datetime


# Down video and sound from a chanel
#
class TikChanel:
    @staticmethod
    def log(cannot, path):
        with open(pa.Path(path) / 'down' / f'cannot - {datetime.datetime.now()}.txt', mode='w', encoding='utf8') as f:
            if cannot is not []:
                f.write('Cannot down files\n')
                for _ in cannot:
                    f.write(_ + '\n')
            else:
                f.write('Success')

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
    def getLinkVideoNoDownload(cls, username, count=10):
        """

        :param username:
        :param count:
        :return: list [id, link]
        """
        a = Tikget()
        for item in cls._getListID(username, count):
            url = f'https://www.tiktok.com/@{username}/video/{item}'
            yield [item, a.videoNo(url)]

    @classmethod
    def getLinkVideoWtDownload(cls, username, count=10):
        """

        :param username:
        :param count:
        :return: list [id, link]
        """
        a = Tikget()
        for item in a.postGetVideoMusic(username, count, 'video'):
            yield item

    @classmethod
    def getLinkSoundDownload(cls, username, count=10):
        """

        :param username:
        :param count:
        :return: list [id, link]
        """
        a = Tikget()
        for item in a.postGetVideoMusic(username, count, 'music'):
            yield item

    @classmethod
    def downChanel(cls, username, option, path, directory, count=10):
        """

        :param username:
        :param count:
        :param option: string follow class con: nowt, wtmusic, nomusic
        :return: files which cannot download
        """
        a = down()
        cannot = []
        if 'no' in option:
            stt = 0
            for _ in cls.getLinkVideoNoDownload(username, count):
                stt += 1
                filename = str(stt) + '. ' + _[0] + ' nowt' + '.mp4'
                if _[1] is not None:
                    a.download(_[1], filename, path, directory)
                else:
                    print('Cannot down file ' + filename + '\n')
                    cannot.append(filename)
        if 'wt' in option:
            stt = 0
            for _ in cls.getLinkVideoWtDownload(username, count):
                stt += 1
                filename = str(stt) + '. ' + _[0] + ' wt' + '.mp4'
                if _[1] is not None:
                    a.download(_[1], filename, path, directory)
                else:
                    print('Cannot down file ' + filename + '\n')
                    cannot.append(filename)
        if 'music' in option:
            stt = 0
            for _ in cls.getLinkSoundDownload(username, count):
                stt += 1
                filename = str(stt) + '. ' + _[0] + '.mp3'
                if _[1] is not None:
                    a.download(_[1], filename, path, directory)
                else:
                    print('Cannot down file ' + filename + '\n')
                    cannot.append(filename)
        return cannot

if __name__ == '__main__':
    test = TikChanel()

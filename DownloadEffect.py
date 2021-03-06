import requests as req
import time
import sys
from pathlib import Path as pa
import os
from time import sleep
from TikTokGet.const import con


class DownloadEffect:

    @staticmethod
    def download(link, filename, path=None, directory=None):
        """
        Download file from link and auto create folder video in __dir if path None
        :param link:
        :param filename:
        :param path:
        :return: false if file exists
        """
        pathOpen = None
        if path is not None or path != '':
            direc = 'down' if directory is None else directory
            path = pa(path) / direc
            if not path.exists():
                os.mkdir(path)
            pathOpen = path / filename
        if pa(pathOpen).is_file():
            print('File is exist')
            return False

        sleep(con.sleeptime)
        r = req.get(link, stream=True)

        start_time = time.time()
        with open(pathOpen, 'wb') as f:
            count = 1
            block_size = 512
            try:
                total_size = int(r.headers.get('content-length'))
                print('file total size :', total_size)
            except TypeError:
                print('using dummy length !!!')
                total_size = 10000000
            print('Downloading file ' + filename)
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
            print('\n')
        return True

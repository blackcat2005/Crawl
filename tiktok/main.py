import sys
import os
from pathlib import Path as path
sys.path.append(str(path(os.path.abspath(__file__)).parent.parent))

from TikTokGet.Tikget import Tikget
from TikTokGet.TikChanel import TikChanel
from DownloadEffect import DownloadEffect as down
from TikTokGet.const import con
from functools import wraps

tik = Tikget()
chan = TikChanel()
download = down()


def infor(func):
    @wraps(func)
    def wrapfun(*args, **kwargs):
        while True:
            try:
                os.system('cls')
                func(*args, **kwargs)
            except ValueError:
                print('Please choose right number')
            except Exception as err:
                print(err)
            else:
                a = input('Continue? (y): ')
                if a != 'y':
                    break
    return wrapfun


@infor
def chanelChoose():
    user_name = input('Username: ')
    print('1. Video no Watermark')
    print('2. Video with Watermark')
    print('3. Sound')
    op = int(input('Choose: '))
    if op < 1 or op > 3:
        raise Exception('Please choose option 1~3')
    count = int(input('How many: '))
    path = input('Path to save: ')
    direc = input('Directory: ')

    sleeptime = float(input('Sleep time (seconds) (default 10secs): '))
    if sleeptime <= 0:
        raise Exception('Sleep time is must higher than 0')
    con.sleeptime = sleeptime if sleeptime is not None else 10.0

    chan.downChanel(user_name, con.option_chanel[str(op)], path, direc, count)


@infor
def videoSingleChoose():
    con.sleeptime = 10.0
    url = input('Url video: ')
    if 'video' not in url:
        raise Exception('Please enter a video url')
    print('1. Get video no watermark')
    print('2. Get video with watermark')
    print('3. Get music')
    a = int(input('Choose: '))
    if a < 1 or a > 3:
        raise Exception('Please enter number 1~3')
    path = input('Path to save: ')
    direc = input('Directory: ')
    link = None
    if a == 1:
        link = tik.videoNo(url)
    elif a == 2:
        link = tik.videoWT(url)
    elif a == 3:
        link = tik.music(url)
    if link is not None:
        download.download(link, tik.getFilename(url), path, direc)
    else:
        print('Cannot get!')


@infor
def origin():
    print('1. Down video, music from chanel username')
    print('2. Down video single')
    print('3. Down music single')
    print('4. Get infor user, video, music')
    print('5. Get trending')
    a = int(input('Choose: '))
    if a > 5 or a < 1:
        raise Exception("Please choose number integer 1~5")
    elif a == 1:
        chanelChoose()
    elif a == 2:
        videoSingleChoose()
origin()

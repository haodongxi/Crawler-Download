import os
import platform
import sys
import ctypes
from urllib.parse import urlencode,quote
import redisutil
import common

# a = False
# print(id(a))
# b = a
# print(id(b))
# print(id(a))
# b = True
# print(id(b))
# print(id(a))
# print(a)

def disk(folder):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024


if __name__ == "__main__":
    lst = redisutil.prange(19806,-1,common.KEY_ALREADY_PAGE)
    for url in lst:
        redisutil.remove(url,common.KEY_ALREADY_PAGE)
    print('删除完毕')

    # from urllib.request import urlopen
    # from bs4 import BeautifulSoup
    # html = urlopen(" http://0122.workarea1.live/view_video.php?viewkey=7b26b2fb66ec41d347ec&page=1&viewtype=basic&category=rf")
    # bsObj = BeautifulSoup(html.read(), 'lxml')
    # str1 =  str(bsObj.title.string)
    # print(str1)
#   print(disk('/Volumes/disk/video/')/1024)
#   url_code_str = quote('https://www.baidu.com')
#   url_code_str = url_code_str.replace('.',r'。')
#   exit(0)
#   print(url_code_str)
    # str1 = "sdasdsadsaasdsdasd"
    # if len(str1)>10:
    #     print(str1[0:10])


    
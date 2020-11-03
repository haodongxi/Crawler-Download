# -*- coding: UTF-8 -*-
import requests, re, redisutil, time, random, threading
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import os
import datetime

cookies = requests.cookies.RequestsCookieJar()
cookies.set("language", "cn_CN", domain=".p06.rocks", path="/")

#--------------------------------------
# 91 的临时站点，可以随时更换
#URL = "http://91porn.com/"
#URL = "http://91.91p17.space/"
#URL = "https://p06.rocks"
# URL = "https://0122.workarea1.live/"
# URL = "http://a.wonderfulday23.live/"
# http://1205.imonitoreo.com.ar/v.php?category=rf&viewtype=basic
# http://1205.imonitoreo.com.ar/
URL = "http://1205.imonitoreo.com.ar/"
KEY = "91"
KEY_SRC = "91_src" # 每个视频源url对于的redis key
KEY_NONE = "91_none"
KEY_ALREADY_PAGE = "91_already_page"
KEY_ALREADY_DOWNLOAD = "91_already_download"

LOG = "f:/log/visit.log"
TORRENT = "f:/sed/"
PARSE_LOG = "f:/log/parse.log"
#----------------------------------------
import os
path = "/".join(LOG.split("/")[0:-1])

if not os.path.exists(TORRENT):
	os.makedirs(TORRENT)

if not os.path.exists(path):
    os.makedirs(path)


'''
  获取访问的主页面
'''
def getNumber():
    r = 0
    while True:
        num = input("请输入你想抓取开始页数:")
        try:
            r = int(num)
            break
        except:
            print("抱歉，您输入的不是有效的数字, 请重新输入.")
            continue
    return r

def getTotalNumber():
    r = 0
    while True:
        num = input("请输入你想抓取总页数:")
        try:
            r = int(num)
            break
        except:
            print("抱歉，您输入的不是有效的数字, 请重新输入.")
            continue
    return r

'''
  获取时长
'''
def getTime():
    r = 0
    while True:
        num = input("请输入想获取的时长(分钟):")
        try:
            r = int(num)
            break
        except:
            print("抱歉，您输入的不是有效的数字, 请重新输入.")
            continue
    return r

'''
   构造随机ip作为请求头访问目标站点
'''
def visit(url):
    randomIP = str(random.randint(0, 255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
    retries = Retry(total=5,backoff_factor=10, status_forcelist=[500,502,503,504])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'X-Forwarded-For': randomIP,
        'Accept-Language':'zh-cn'}
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=headers, cookies=cookies,timeout=10).content
    return html


def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path) 
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


def getCurrentDate():
    today=datetime.date.today()
    formatted_today=today.strftime('%y%y%m%d')
    return formatted_today+'-mf'

if __name__ == "__main__":
    print(getCurrentDate())
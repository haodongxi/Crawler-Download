import urllib.request as request
import random
import redis
import threading
from threading import Lock
import ctypes
import os
import platform
import sys
from urllib import error
import time
from urllib.parse import urlencode
import json

import demjson
import common
import redisutil
client = redis.StrictRedis("localhost", 6379)
rlock = threading.RLock()
thread_stop_flag = False
file_name = ""
dir_path = r"/Volumes/MongoDBStudy/.supergate$/.a/.a/bin/"

def download_enter(**kwargs):
    global rlock
    global thread_stop_flag
    start = kwargs["start"]
    end = kwargs["end"]
    index = kwargs["index"]
    url = kwargs['url']
    data_list = kwargs['datalist']
    randIP = kwargs['randIP']
    req = request.Request(url)
    req.add_header(
        'User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0")
    req.add_header('X-Forwarded-For', randIP)
    if end == -1:
        req.add_header('Range', 'bytes='+str(start)+'-')
    else:
        req.add_header('Range', 'bytes='+str(start)+'-'+str(end))
    if thread_stop_flag:
        print(threading.current_thread().name+'因其他出错，停止此线程')
        return
    response = request.urlopen(req,timeout=10)
    file_size = int(response.getheader("Content-Length"))
    bytes_received = 0
    bytes_data = b''
    code = response.code
    print(threading.current_thread().name+'   code  '+str(code))
    print(threading.current_thread().name+'开始下载')
    try:
            while bytes_received / file_size != 1:
                if thread_stop_flag:
                    print(threading.current_thread().name+'因其他出错，停止此线程')
                    return
                _buffer = response.read(1024 * 1024)
                bytes_data +=_buffer
                bytes_received += len(_buffer)
                print(threading.current_thread().name +
                      " 已下载 " + str(bytes_received / file_size))
            rlock.acquire()
            data_list[index] = bytes_data
            rlock.release()
    except Exception as e:
            thread_stop_flag = True
            print(threading.current_thread().name+'下载片出错')
            print(e)
    
def sm_download(filesize,url):
    global thread_stop_flag
    global dir_path
    global file_name
    thread_list = []
    thread_count = 20
    data_list = {}
    if filesize < thread_count:
        thread_count = 1
    sc_size = filesize//thread_count
    randIP = str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + \
        "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
    thread_stop_flag = False
    for i in range(0,thread_count):
        start = i*sc_size
        end = start+sc_size-1
        if i == thread_count-1:
            end = -1
        name = "download" + str(i)
        t = threading.Thread(target=download_enter, name=name, kwargs={"start":start,"end":end,"index":i,"url":url,"datalist":data_list,"randIP":randIP})
        thread_list.append(t)   

    for t in thread_list:
        time.sleep(0.3)
        t.start()

    for t in thread_list:
        t.join()
    compose_result = True
    if disk(dir_path)/1024<0.5 :
        exit(0)
    
    date_path = dir_path + common.getCurrentDate()
    common.mkdir(date_path)
    file_path = date_path +'/'+ file_name + ".mp4"
    with open(file_path, 'wb') as dst_file:
            for index in range(0,thread_count):
                if data_list.__contains__(index):
                    buffer_data = data_list[index]
                    if isinstance(buffer_data,bytes):
                        dst_file.write(buffer_data)
                    else:
                        print('该片无数据流，即为下载失败'+str(index))
                        compose_result = False
                        break
                else:
                    print('该片为空，即为下载失败'+str(index))
                    compose_result = False
                    break
    if compose_result:
        print('合成成功')
    else:
        print('合成失败')
        if os.path.exists(file_path):
            os.remove(file_path)
            print('删除文件')

def normal_download(file_size,response,url):
    global dir_path
    global file_name
    bytes_received = 0
    try:
        if disk(dir_path)/1024<0.5 :
            exit(0)
        date_path = dir_path + common.getCurrentDate()
        common.mkdir(date_path)
        file_path =  date_path+'/' +file_name + ".mp4"
        with open(file_path, 'wb') as dst_file:
            while bytes_received / file_size != 1:
                _buffer = response.read(1024 * 1024)
                bytes_received += len(_buffer)
                dst_file.write(_buffer)
                print(threading.current_thread().name +
                      " 已下载 " + str(bytes_received / file_size))
    except KeyboardInterrupt:
        raise KeyboardInterrupt(
            "Interrupt signal given. Deleting incomplete video.")

def disk(folder):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024


def download(url):
    global dir_path
    print('下载的url  '+url)
    randIP = str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + \
        "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
    req = request.Request(url)
    req.add_header(
        'User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0")
    req.add_header('X-Forwarded-For', randIP)
    req.add_header('Range', 'bytes=0-')
    # ('Accept-Ranges', 'bytes')
    try:
        response = request.urlopen(req,timeout=10)
        file_size = 0
        code = response.code
        if code == 206:
            # 分片下载
            #'bytes 0-20/104629316'
            range_length = response.getheader('Content-Range')
            file_size_list = range_length.split(r'/')
            if len(file_size_list)>0 :
                file_size = int(file_size_list[-1])
                sm_download(file_size,url)
            else :
                pass
        elif code == 200:
            file_size = int(response.getheader("Content-Length"))
            #正常下载
            normal_download(file_size,response,url)
        else:
            print('获取contetnlegth报错')
    except error.HTTPError as e:
         print(e.code)
    except Exception as e:
        print(e)#'http://23.225.233.3//mp43/366445.mp4?st=ZADNhKoTVFRQwxKs2BW5XA&e=1587895189'
        print('未知错误')
    

def enter(**kwargs):
    start = kwargs["start"]
    end = kwargs["end"]
    global file_name
    global dir_path
    lst = client.lrange("91_src", start, end)
    for a in lst:
        src_map_str = a.decode("utf-8")
        title = ""
        if not r'title' in src_map_str and not r'src' in src_map_str:
            src = src_map_str
        else :
            src_map = demjson.decode(src_map_str)
            src = src_map['src']
            title = src_map['title']
        if not title or len(title) == 0:
            title = str(random.randint(11111111111,99999999999999999))
        title = title.replace("\t","")
        title = title.replace("\n","")
        title = title.replace("\r","")
        file_name = title
        # file_path = dir_path + file_name + ".mp4"
        date_path = dir_path + common.getCurrentDate()
        file_path =  date_path+'/' +file_name + ".mp4"
        if os.path.exists(file_path) or redisutil.exists(a,common.KEY_ALREADY_DOWNLOAD):
            print('已经下载的url，删除')
            client.lrem("91_src", 0, a)
            redisutil.add(a,common.KEY_ALREADY_DOWNLOAD)
            continue
        if not r'http://v2' in src :
            download(src)
            print(threading.current_thread().name,
                      " 下载 ", src, " 完成， 从redis 删除")
            client.lrem("91_src", 0, a)
            redisutil.add(a,common.KEY_ALREADY_DOWNLOAD)
        else :
            print('无法下载的url-v2')
            client.lrem("91_src", 0, a)
            redisutil.add(a,common.KEY_ALREADY_DOWNLOAD)

if __name__ == "__main__":
    # thread_list = []

    # for i in range(1, 6):
    # 	start = (i - 1) * 4000 + 1
    # 	end = i * 4000 + 1
    # 	t = threading.Thread(target=enter, name="a" + str(i),kwargs={'start':start, 'end':end})
    # 	thread_list.append(t)

    # for t in thread_list:
    # 	t.start()

    # for t in thread_list:
    # 	t.join()

    # print("over")
    end = int(redisutil.total(common.KEY_SRC))
    enter(start=1, end=end)


# -*- coding: UTF-8 -*-
import requests, re, redis, redisutil, time, random
from pyquery import PyQuery as pq
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import threading
import common
from bs4 import BeautifulSoup
import js2py

# 将列表页插入redis
def parse(url, c, ts):
    try:
        d = pq(common.visit(url))
        # 旧版获取src
        #src = d("video").find("source").attr("src")
        # 新版获取src
        src = d("#player_one script").text()
        src = src[20:-8]
        context = js2py.EvalJs()
        js_code = ''';var encode_version = 'sojson.v5', lbbpm = '__0x33ad7',  __0x33ad7=['QMOTw6XDtVE=','w5XDgsORw5LCuQ==','wojDrWTChFU=','dkdJACw=','w6zDpXDDvsKVwqA=','ZifCsh85fsKaXsOOWg==','RcOvw47DghzDuA==','w7siYTLCnw=='];(function(_0x94dee0,_0x4a3b74){var _0x588ae7=function(_0x32b32e){while(--_0x32b32e){_0x94dee0['push'](_0x94dee0['shift']());}};_0x588ae7(++_0x4a3b74);}(__0x33ad7,0x8f));var _0x5b60=function(_0x4d4456,_0x5a24e3){_0x4d4456=_0x4d4456-0x0;var _0xa82079=__0x33ad7[_0x4d4456];if(_0x5b60['initialized']===undefined){(function(){var _0xef6e0=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x221728='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0xef6e0['atob']||(_0xef6e0['atob']=function(_0x4bb81e){var _0x1c1b59=String(_0x4bb81e)['replace'](/=+$/,'');for(var _0x5e3437=0x0,_0x2da204,_0x1f23f4,_0x3f19c1=0x0,_0x3fb8a7='';_0x1f23f4=_0x1c1b59['charAt'](_0x3f19c1++);~_0x1f23f4&&(_0x2da204=_0x5e3437%0x4?_0x2da204*0x40+_0x1f23f4:_0x1f23f4,_0x5e3437++%0x4)?_0x3fb8a7+=String['fromCharCode'](0xff&_0x2da204>>(-0x2*_0x5e3437&0x6)):0x0){_0x1f23f4=_0x221728['indexOf'](_0x1f23f4);}return _0x3fb8a7;});}());var _0x43712e=function(_0x2e9442,_0x305a3a){var _0x3702d8=[],_0x234ad1=0x0,_0xd45a92,_0x5a1bee='',_0x4a894e='';_0x2e9442=atob(_0x2e9442);for(var _0x67ab0e=0x0,_0x1753b1=_0x2e9442['length'];_0x67ab0e<_0x1753b1;_0x67ab0e++){_0x4a894e+='%'+('00'+_0x2e9442['charCodeAt'](_0x67ab0e)['toString'](0x10))['slice'](-0x2);}_0x2e9442=decodeURIComponent(_0x4a894e);for(var _0x246dd5=0x0;_0x246dd5<0x100;_0x246dd5++){_0x3702d8[_0x246dd5]=_0x246dd5;}for(_0x246dd5=0x0;_0x246dd5<0x100;_0x246dd5++){_0x234ad1=(_0x234ad1+_0x3702d8[_0x246dd5]+_0x305a3a['charCodeAt'](_0x246dd5%_0x305a3a['length']))%0x100;_0xd45a92=_0x3702d8[_0x246dd5];_0x3702d8[_0x246dd5]=_0x3702d8[_0x234ad1];_0x3702d8[_0x234ad1]=_0xd45a92;}_0x246dd5=0x0;_0x234ad1=0x0;for(var _0x39e824=0x0;_0x39e824<_0x2e9442['length'];_0x39e824++){_0x246dd5=(_0x246dd5+0x1)%0x100;_0x234ad1=(_0x234ad1+_0x3702d8[_0x246dd5])%0x100;_0xd45a92=_0x3702d8[_0x246dd5];_0x3702d8[_0x246dd5]=_0x3702d8[_0x234ad1];_0x3702d8[_0x234ad1]=_0xd45a92;_0x5a1bee+=String['fromCharCode'](_0x2e9442['charCodeAt'](_0x39e824)^_0x3702d8[(_0x3702d8[_0x246dd5]+_0x3702d8[_0x234ad1])%0x100]);}return _0x5a1bee;};_0x5b60['rc4']=_0x43712e;_0x5b60['data']={};_0x5b60['initialized']=!![];}var _0x4be5de=_0x5b60['data'][_0x4d4456];if(_0x4be5de===undefined){if(_0x5b60['once']===undefined){_0x5b60['once']=!![];}_0xa82079=_0x5b60['rc4'](_0xa82079,_0x5a24e3);_0x5b60['data'][_0x4d4456]=_0xa82079;}else{_0xa82079=_0x4be5de;}return _0xa82079;};if(typeof encode_version!=='undefined'&&encode_version==='sojson.v5'){function strencode(_0x50cb35,_0x1e821d){var _0x59f053={'MDWYS':'0|4|1|3|2','uyGXL':function _0x3726b1(_0x2b01e8,_0x53b357){return _0x2b01e8(_0x53b357);},'otDTt':function _0x4f6396(_0x33a2eb,_0x5aa7c9){return _0x33a2eb<_0x5aa7c9;},'tPPtN':function _0x3a63ea(_0x1546a9,_0x3fa992){return _0x1546a9%_0x3fa992;}};var _0xd6483c=_0x59f053[_0x5b60('0x0','cEiQ')][_0x5b60('0x1','&]Gi')]('|'),_0x1a3127=0x0;while(!![]){switch(_0xd6483c[_0x1a3127++]){case'0':_0x50cb35=_0x59f053[_0x5b60('0x2','ofbL')](atob,_0x50cb35);continue;case'1':code='';continue;case'2':return _0x59f053[_0x5b60('0x3','mLzQ')](atob,code);case'3':for(i=0x0;_0x59f053[_0x5b60('0x4','J2rX')](i,_0x50cb35[_0x5b60('0x5','Z(CX')]);i++){k=_0x59f053['tPPtN'](i,len);code+=String['fromCharCode'](_0x50cb35[_0x5b60('0x6','s4(u')](i)^_0x1e821d['charCodeAt'](k));}continue;case'4':len=_0x1e821d[_0x5b60('0x7','!Mys')];continue;}break;}}}else{alert('');};'''
        context.execute(js_code)
        src = context.eval(src)
        src = pq(src)
        src = src("source").attr("src")
        # 新版获取src
        if src != None:
            m = common.visit(url)
            soup = BeautifulSoup(m, "lxml")
            title =  str(soup.title.string)
            title = title.replace(' ',"")
            title = title.replace('/',"")
            title = title.replace("\\","")
            title = title.replace(",","")
            title = title.replace("，","")
            title = title.replace("。","")
            title = title.replace(".","")
            title = title.replace("\t","")
            title = title.replace("\n","")
            title = title.replace("\r","")
            title = title.replace("'","")
            title = title.replace("\"","")
            title = title.replace("‘","")
            title = title.replace("","")
            title = title.replace(" ","")
            title = title.replace("?","")
            title = title.replace("？","")
            if len(title)>15:
                title = title[0:15]
            con = soup.find(name="div", attrs={"class": "boxPart"}).text
            con = "".join(con.split())
            t = con.split(":")
            times = int(t[1])
            ts = int(ts)
            if times >= ts:
                if '//mp' in src :
                    src = src.replace('//mp','/mp')
                print( threading.current_thread().name,  " insert into redis ", src)
                src_title_map = {'src':src,'title':title}
                if not redisutil.exists(str(src_title_map),common.KEY_ALREADY_DOWNLOAD):
                    redisutil.add(str(src_title_map), common.KEY_SRC)
                else:
                    print('该url已下载'+src)
            else:
                print(threading.current_thread().name,  src, "Not enough time")
        else:
            print(threading.current_thread().name,  src, "解析为None, 插入 redis_error")
            # redisutil.add(src, common.KEY_NONE)
    except Exception as e:
        print(e)#'http://23.225.233.3//mp43/366445.mp4?st=ZADNhKoTVFRQwxKs2BW5XA&e=1587895189'
        print('src----visit--error')

def enter(**kwargs):
    start = kwargs["start"]
    end = kwargs["end"]
    ts = kwargs["ts"]
    c = redisutil.connect()
    lst = c.lrange(common.KEY, int(start), int(end))

    for a in lst:
         print(threading.current_thread().name,  " parsing url ", a)
         parse(a, c, ts)
         c.lrem(common.KEY, 0, a)
         redisutil.add(a,common.KEY_ALREADY_PAGE)
         time.sleep(0.1)
    with open(common.PARSE_LOG, "a") as f:
        f.write(threading.current_thread().name + " 已经解析完毕.\n")

def start():
    thread_list = []
    total = redisutil.total(common.KEY)
    ts = 0 #common.getTime()
    page_size = 0
    thread_total = 5

    if total <= 5:
        page_size = 1
        thread_total = total
    else:
        page_size = total / 5

    for t in range(1, thread_total + 1):
        start = (t - 1) * page_size + 1
        end = t * page_size + 1
        name = "a" + str(t)
        t = threading.Thread(target=enter, name=name, kwargs={"start":start, "end":end,"ts":ts})
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    print("all thread over")

if __name__ == "__main__":
    start()
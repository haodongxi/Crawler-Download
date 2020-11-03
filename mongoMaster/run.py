# -*- coding: UTF-8 -*-
import parse_list, parse_src, time,src2file,download_thread,common,redisutil

def start():    
    try:
        print("即将启动解析列表程序")
        parse_list.start()

        # 睡眠5分钟后启动
        print("即将启动解析视频程序")
        #time.sleep(2)
        parse_src.start()

        # time.sleep(3)
        end = int(redisutil.total(common.KEY_SRC))
        download_thread.enter(start=1, end=end)

    except Exception as e:
        print(e)
        print('整个程序出错')
    # 写入文件
    # src2file.writeUrl2File()
if __name__ == "__main__":
    start()

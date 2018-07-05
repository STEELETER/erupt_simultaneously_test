import json
import threading
import time

import sys



from PyQt5.QtWidgets import QApplication

from modules.notice.controller import add
from modules.trans.download import Downloader
# from modules.trans.trans_pool import up_pool, add_to_pool, pool, down_pool
from modules.trans.trans_pool import up_pool, down_pool

from modules.trans.upload import Uploader
from modules.utils.conf import updown_serv_addr
from modules.utils.db import open_db
from modules.notice import controller as notice



'''
'{"id":"xxxxx","up_from":"xxxxxxxx","up_to":"xxxxxxx"}'
'''
def add_item_up(item,addr=updown_serv_addr):
    # add_to_pool(json.loads(item)['id'],False)

    # up_pool.apply_async(func=Uploader,args=(item,addr))

    # up_pool.submit(Uploader,item,addr)
    a = Uploader(item,addr)
    a.wait();



'''
'[{"id":"xxxxx","up_from":"xxx","up_to":"xxx"},{"id":"xxxxx","up_from":"xxx","up_to":"xxx"}...]'

'''
def add_list_up(up_json_list,addr=updown_serv_addr):
    up_list =  json.loads(up_json_list)
    for item in up_list:
        add_item_up('{"id":"%s","up_from":"%s","up_to":"%s"}'%(str(item["id"]),str(item['up_from']),str(item['up_to'])),addr)

'''
'{"id":"xxxxx","down_from":"xxxxxxxx","down_to":"xxxxxxx"}'
'''
def add_item_down(item,addr=updown_serv_addr):
    # add_to_pool(json.loads(item)['id'],False)
    down_pool.submit(Downloader,item,addr)


'''
'[{"id":"xxxxx","down_from":"xxx","down_to":"xxx"},{"id":"xxxxx","down_from":"xxx","down_to":"xxx"}...]'

'''
def add_list_down(down_json_list,addr=updown_serv_addr):
    up_list =  json.loads(down_json_list)
    for item in up_list:
        add_item_down('{"id":"%s","down_from":"%s","down_to":"%s"}'%(str(item["id"]),str(item['down_from']),str(item['down_to'])),addr)


def test():

    notice.add('')

if __name__ == '__main__': # 使用该if正常运行
    app = QApplication(sys.argv)
    # #
    # # multiprocessing.freeze_support()
    notice.start()

    # # time.sleep(6)
    # up_pool = multiprocessing.Pool(processes=2)
    # down_pool= multiprocessing.Pool(processes=2)
    add_list_up('[{"id":"1","up_from":"F:/eclipse-jee-kepler-SR2-win32.zip","up_to":"D:/eclipse-jee-kepler-SR2-win32.zip"}]')
                # ',{"id":"2","up_from":"F:/cn_visio_professional_2016_x86_x64_dvd.rar","up_to":"D:/cn_visio_professional_2016_x86_x64_dvd.rar.zip"},{"id":"3","up_from":"F:/Adobe Photoshop CS6  roustar31中文特别版.exe","up_to":"D:/Adobe Photoshop CS6  roustar31中文特别版.exe"}]')
                #   ,')

    # subThread.wait();
    #
    #
    # time.sleep(3)
    # if pool['1']:
       # pool['1'].suspend()
       #   pool['1'].resume()

    # time.sleep(6)
    # pool['1'].resume()
    # print(b'123'+b'456')
    sys.exit(app.exec_())
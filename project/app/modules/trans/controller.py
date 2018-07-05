import json
import time

from modules.trans.download import Downloader
from modules.trans.trans_pool import add_to_pool, up_pool, pool
from modules.trans.upload import Uploader
from modules.utils.check import check_sysnum
from modules.utils.conf import updown_serv_addr

'''
'{"sysnum":"868608","id"："xxx","up_from":"xxxxxxxx","up_to":"xxxxxxx"}'
'''
def add_item_up(item,addr=updown_serv_addr):
    add_to_pool(json.loads(item)['id'],False)
    up_pool.submit(Uploader,item,addr)


'''
'{"sysnum":"868608","up_list":[{"id"："xxx","up_from":"xxx","up_to":"xxx"},{"id"："xxx","up_from":"xxx","up_to":"xxx"}...]}'

'''
def add_list_up(up_json_list,addr=updown_serv_addr):
    list_dict = json.loads(up_json_list)
    sysnum = list_dict['sysnum']
    check_sysnum(sysnum)

    up_list =  list_dict['up_list']
    for item in up_list:
        add_item_up('{"sysnum":"%s","id":"%s","up_from":"%s","up_to":"%s"}'%(str(sysnum),str(item["id"]),str(item['up_from']),str(item['up_to'])),addr)

'''
'{"sysnum":"868608","id"："xxx","down_from":"xxxxxxxx","down_to":"xxxxxxx"}'
'''
def add_item_down(item,addr=updown_serv_addr):
    add_to_pool(json.loads(item)['id'],False)
    up_pool.submit(Downloader,item,addr)


'''
'{"sysnum":"868608","down_list":[{"id"："xxx","down_from":"xxx","down_to":"xxx"},{"id"："xxx","down_from":"xxx","down_to":"xxx"}...]}'

'''
def add_list_down(down_json_list,addr=updown_serv_addr):
    list_dict = json.loads(down_json_list)
    sysnum = list_dict['sysnum']
    check_sysnum(sysnum)

    up_list =  list_dict['down_list']
    for item in up_list:
        add_item_down('{"sysnum":"%s","id":"%s","down_from":"%s","down_to":"%s"}'%(str(sysnum),str(item["id"]),str(item['down_from']),str(item['down_to'])),addr)


if __name__=="__main__":
    # dict = {}
    # dict['sysnum'] = '868608'
    # dict['source'] = {'fpath':'xxxx','fsize':'xxxx'}
    # print(os.path.getsize('C:/Users/Administrator/Desktop/new_app/src/web/web1.zip'))

    # print(pysm4.sm4._byte_pack(b'sssssssss'))

    add_list_down('{"sysnum":"868608","down_list":[{"id": "3", "down_from": "D:/Sublime Text 3/python3.3.zip", "down_to": "E:/VS.zip"}]}')
    time.sleep(3)
    # ,{"id": "1", "down_from": "E:/text.zip", "down_to": "D:/text.zip"}
    # ,
    # {"id": "2", "down_from": "E:/new_data.zip", "down_to": "D:/new_data.zip"}
    # if pool['3']:
    #     print(pool['3'].suspend())
from concurrent.futures import ThreadPoolExecutor

import multiprocessing

from common.conf import up_thread_num, down_thread_num

pool = {}
up_pool = ThreadPoolExecutor(max_workers=up_thread_num)# 创建一个最大可容纳x个task的线程池
down_pool = ThreadPoolExecutor(max_workers=down_thread_num)# 创建一个最大可容纳x个task的线程池

# up_pool = multiprocessing.Pool(processes=up_thread_num)
# down_pool= multiprocessing.Pool(processes=down_thread_num)



def add_to_pool(id,value):
    pool[id] = value


updown_list = []
def test(item):
    updown_list.append(item)
    print(updown_list)

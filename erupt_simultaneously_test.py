
import gevent
import random
import time


# from gevent import monkey
# monkey.patch_all()


def task(pid):
    gevent.sleep(random.randint(0, 2) * 0.001)
    # 模拟真实环境，等待时间随机，同步：0.183，顺序执行；异步：0.012，随机执行。
    # gevent.sleep(0.1)  # 如果等待时间固定，同步：10秒，顺序执行；异步：0.1秒多，表现为顺序执行。
    print('Task', pid, 'done')


def synchronous():  # 同步
    # for i in range(1,100):
    for i in range(100):
        task(i)


def asynchronous():  # 异步
    threads = [gevent.spawn(task, i) for i in range(100)]
    gevent.joinall(threads)


print('Synchronous:')
start = time.time()
synchronous()
stop = time.time()
print(stop - start)


print('Asynchronous:')
start = time.time()
asynchronous()
stop = time.time()
print(stop - start)


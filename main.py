#!/usr/bin/env python3
import requests
from CDaemon import CDaemon
import os,time,sys
import schedule

'''
打印错误
'''
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#---------------- start ----------------
### 功能代码起点，代码写在这里就可以了

# !!! 这里需要改
url = 'https://v2.chengjunjie.com/login.html?api.post'

# !!! 请求Headers
headers = {
}

# !!! Data [a Python object (dict)]
data = {
  "key1": '你的数据'
}

# 发送请求
def postJSONData(url, data, headers):
  try:
    res = requests.post(url = url, json = data, headers= headers)
    if (res.status_code == 200):
      return True
    else:
      return False
  except Exception as err:
    eprint(err)

# !!!!!你的代码写在这里就好了
def job():
    print("I'm working...")
    # postJSONData(url, data, headers)

def main():
    # 定时器教程：https://pypi.org/project/schedule/
    schedule.every(10).seconds.do(job)
    while(True):
        schedule.run_pending()
        time.sleep(1)

#---------------- end ----------------
### 功能代码终点


# 下面的程序不需要改动

class ClientDaemon(CDaemon):
  def __init__(self, name, pid_file_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=0o022, verbose=1):
    CDaemon.__init__(self, pid_file_path, stdin, stdout, stderr, home_dir, umask, verbose)
    self.name = name #派生守护进程类的名称
 
  def run(self):
    main()


if __name__ == '__main__':
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)
    p_name = 'my_app' #守护进程名称
    pid_fn = './daemon.pid' #守护进程pid文件的绝对路径
    out_fn = './daemon.out.log' #守护进程日志文件的绝对路径
    err_fn = './daemon.err.log' #守护进程启动过程中的错误日志,内部出错能从这里看到
    cD = ClientDaemon(p_name, pid_fn, stdout=out_fn, stderr=err_fn, verbose=1, home_dir='.')
 
    if sys.argv[1] == 'start':
        cD.start()
    elif sys.argv[1] == 'stop':
        cD.stop()
    elif sys.argv[1] == 'restart':
        cD.restart()
    elif sys.argv[1] == 'status':
        alive = cD.is_running()
        if alive:
            print('process [%s] is running ......' % cD.get_pid())
        else:
            print('daemon process [%s] stopped' %cD.name)
    else:
        print('invalid argument!')
        print(help_msg)

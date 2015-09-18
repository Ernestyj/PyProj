#coding: utf-8
import os, sys, time, subprocess, thread
from Tools.Scripts.treesync import raw_input

__author__ = 'Jian'

# 当前文件路径
path = os.path.abspath(__file__)

# 当前文件修改时间
mtime = os.stat(path).st_mtime

# 主进程为控制器，不做功能处理
if not os.environ.get('is_child'):
    argv = [sys.executable] + sys.argv
    environ = os.environ.copy()

    # 给子进程标记，不做控制功能
    environ['is_child'] = 'true'

    # 先开一个子进程，执行程序功能
    p = subprocess.Popen(argv, env=environ)

    while True:
        if os.stat(path).st_mtime != mtime:
            mtime = os.stat(path).st_mtime
            p = subprocess.Popen(argv, env=environ)
            print('reloaded')
        time.sleep(1)


# 程序功能部分
def main():
    print('try to modifdy this part and save!')
    raw_input() # 模拟监听请求

# 新线程执行功能
thread.start_new_thread(main, ())

# 主线程监听结束
while True:
    if mtime < os.stat(path).st_mtime:
        sys.exit(0)
    time.sleep(1)

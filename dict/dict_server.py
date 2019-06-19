"""
    dict 服务端

    功能:业务逻辑处理
    模型多进程tcp并发
"""
from operation_db import *
from socket import *
from multiprocessing import Process
import signal,sys
from time import sleep

# 全局变量
HOST = "0.0.0.0"
PORT = 8956
ADDR = (HOST,PORT)
# 数据库对象
db = Database()

# 注册处理
def do_register(connfd, data):
    # 对数据进行处理-->按照空格切割
    tmp = data.split(" ")
    name = tmp[1]
    password = tmp[2]
    if db.register(name, password):
        connfd.send(b"OK")
    else:
        connfd.send(b"Fail")

# 登录处理
def do_login(connfd,data):
    tmp = data.split(" ")
    name = tmp[1]
    password = tmp[2]
    if db.login(name,password):
        connfd.send(b"OK")
    else:
        connfd.send(b"Fail")

# 查询单词
def do_query(connfd,data):
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    # 查询单词同时,插入历史记录
    db.insert_history(name,word)
    # 在数据库中查询单词,找的了返回解释,没找到返回None
    mean = db.query(word)
    if not mean:
        connfd.send(b"Nothing")
    else:
        # 将单词和解释进行拼接并发送到服务端
        msg = "%s : %s"%(word,mean)
        connfd.send(msg.encode())

# 历史记录
def do_hist(connfd, data):
    name = data.split(" ")[1]
    data = db.history(name)
    if not data:
        connfd.send(b"Fail")
        return
    connfd.send(b"OK")
    send_hist(connfd, data)

# 遍历在数据库查询返回的结果,并发送到服务端
def send_hist(connfd, data):
    for i in data:
        # i --> (name,word,time)
        msg = "%s  %-16s  %s" % i
        sleep(0.1)  # 防止沾包
        connfd.send(msg.encode())
    sleep(0.1)
    connfd.send(b"##")  # 发送 ## 表示发送结束


# 处理客户端请求
def requst(connfd):
    db.create_cursor()  # 生成游标
    while True:
        data = connfd.recv(1024).decode()
        # print(connfd.getpeername(),":",data)
        if not data or data[0] == "E":
            sys.exit()
        elif data[0] == "R":
            do_register(connfd, data)
        elif data[0] == "L":
            do_login(connfd, data)
        elif data[0] == "Q":
            do_query(connfd,data)
        elif data[0] == "H":
            do_hist(connfd,data)


# 搭建网络
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print("Listen the port 8956")
    while True:
        try:
            coonfd,addr = sockfd.accept()
            print("Connect from:",addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        # 为客户端创建子进程
        p = Process(target = requst, args = (coonfd, ))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()





















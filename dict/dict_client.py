"""
    dict 客户端

    功能:根据用户输入,发送请求,得到结果
    结构:  一级界面 --> 注册  登录  退出
          二级界面 --> 查单词  历史记录  注销
"""
from socket import *
from getpass import getpass  # 运行使用终端
import sys

# 服务器地址
ADDR = ("127.0.0.1", 8956)
# 功能函数都需要套接字,定义为全局变量
sockfd = socket()
sockfd.connect(ADDR)

# 注册函数
def do_register():
    while True:
        name = input("User:")
        password = getpass()  # 隐藏输入
        password_ = getpass("Again:")
        # 确定输入用户名和密码格式
        if (" " in name) or (" " in password):
            print("用户名或密码不能有空格")
            continue
        if password != password_:
            print("两次密码输入不一致")
            continue
        return register_send_msg(name, password)

# 注册函数-->将姓名密码发送给服务端处理
def register_send_msg(name, password):
    msg = "R %s %s" % (name, password)
    sockfd.send(msg.encode())  # 发送请求
    data = sockfd.recv(128).decode()  # 接收反馈信息
    if data == "OK":
        print("注册成功")
        login(name)  # 注册成功,进入二级界面
    else:
        print("注册失败")
    return

# 登录函数
def do_login():
    name = input("User:")
    password = getpass()
    # 确定输入用户名和密码格式
    if (" " in name) or (" " in password):
        print("用户名或密码不能有空格")
    return login_send_msg(name, password)

# 登录函数 --> 将姓名密码发送给服务端处理
def login_send_msg(name, password):
    msg = "L %s %s" % (name, password)
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == "OK":
        print("登陆成功")
        login(name)  # 登陆成功,进入二级界面
    else:
        print("登录失败,请重新登录") # 登录失败返回到一级界面
    return

# 单词查找
def do_query(name):
    while True:
        word = input("Word>>>")
        if word == "##":  # 结束单词查询
            break
        msg = "Q %s %s"%(name,word)
        sockfd.send(msg.encode())
        # 服务端直接发送查询结果(或者没找到)
        data = sockfd.recv(2048).decode()
        print(data)

# 历史记录
def do_hist(name):
    # msg = "H %s"%name
    sockfd.send(("H %s"%name).encode())
    data = sockfd.recv(128).decode()
    if data == "OK":
        # 循环接收查询到的历史记录
        while True:
            data = sockfd.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print("Nothing")

# 二级界面
def login(name):
    while True:
        print("""
        =================Query=================
        
           1.查单词     2.历史记录      3.注销
        
        =======================================
        """)
        cmd = input("请输入选项:")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_hist(name)
        elif cmd == "3":
            return    # 退回到一级界面
        else:
            print("请输入正确选项")

# 搭建客户端网络
def main():
    while True:
        print("""
        ================Welcome================
                                            
            1.注册        2.登录        3.退出   
                                             
        =======================================
        """)
        cmd = input("请输入选项:")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            sockfd.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")


if __name__ == '__main__':
    main()
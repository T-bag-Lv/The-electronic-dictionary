"""
    dict  数据库处理
    功能:提供服务端所有数据库操作
"""
import pymysql
import hashlib
# 加密符号
SALT = "*&%^$"

class Database:
    def __init__(self,host = "localhost",
                 port = 3306,
                 user = "root",
                 passwd = "123456",
                 charset = "utf8",
                 database = "dict"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.database = database
        self.connect_db()  # 连接数据库

    # 连接数据库
    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.passwd,
                                  database = self.database,
                                  charset = self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.db.close()

    # 注册操作
    def register(self,name, password):
        sql = "select * from user where name ='%s'"%name
        self.cur.execute(sql)
        # 如果有查询结果则name存在,并以元组形式返回
        r = self.cur.fetchone()
        if r:
            return False

        # 密码加密处理
        hash = hashlib.md5((name + SALT).encode())
        hash.update(password.encode())  # 算法加密
        passwd = hash.hexdigest()  # 提取加密后的密码

        return self.insert_user(name, passwd)

    # 将注册用户插入数据库
    def insert_user(self, name, passwd):
        sql = "insert into user (name,password) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    # 登录处理
    def login(self,name,password):
        hash = hashlib.md5((name + SALT).encode())
        hash.update(password.encode())  # 算法加密
        passwd = hash.hexdigest()

        # 数据库查找用户
        sql = "select * from user where name ='%s' and password = '%s'"%(name,passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    # 查询单词
    def query(self,word):
        sql = "select mean from words where word = '%s'"%word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0] # 返回值为元组

    # 将单词查询信息插入数据库
    def insert_history(self, name, word):
        sql = "insert into hist (name, word) values (%s, %s)"
        try:
            self.cur.execute(sql,[name, word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    # 查询历史记录
    def history(self,name):
        # 将数据按照时间降序,并返回10个记录
        sql = "select name, word, time from hist where \
              name = '%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()








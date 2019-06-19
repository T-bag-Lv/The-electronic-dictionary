"""
    练习:
    dict下创建数据表 words
    id  word  mean三个字段,要求存储单词本
"""
import pymysql
import re

fd = open("dict.txt","r")

# 连接数据库
db = pymysql.connect(host = "localhost",
                     port = 3306,
                     user = "root",
                     password = "123456",
                     database = "dict",
                     charset = "utf8")

# 获取游标(用于进行数据操作的对象,承载操作结果)
cur = db.cursor()

# 执行sql语句

sql = "insert into words (word, mean) values (%s, %s)"

# 获取 word 和 mean
for line in fd:
    # 利用正则表达式匹配字符串,并返回子组内容
    tup = re.findall(r"(\S+)\s+(.*)",line)[0]
    # # 普通写法切割数据
    # # 将读到的数据按空格切割,存入列表
    # list_ = line.split(" ")
    # # 列表第一个元素为word
    # word = list_[0]
    # # 将列表内容从第二个元素切片,并且用空格连接合并成一个新字符串,最后用strip()函数将字符串开头和结尾的空格删除
    # mean = " ".join(list_[1:]).strip()
    try:
        cur.execute(sql,tup)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

# 关闭数据库
cur.close()
db.close()


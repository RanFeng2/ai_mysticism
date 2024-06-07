import pymysql

try:
    conn = pymysql.connect(
        host='xxxx',            # 数据库地址
        port=xxxx,              # 端口
        user='xxxxx',           # 用户名
        password='xxxx',        # 密码
        database='xxxxx'        # 数据库名
    )
    print("连接成功！")
except Exception as e:
    print("连接失败：", e)
    
# 执行SQL查询
cursor = conn.cursor()
cursor.execute('SELECT * FROM User')

# 获取查询结果
results = cursor.fetchall()
for row in results:
    print(row)

# 关闭数据库连接
conn.close()
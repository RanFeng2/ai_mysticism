import pymysql

try:
    conn = pymysql.connect(
        host='8.130.32.234',
        port=3306,
        user='ai-mysticism',  # 更正用户名
        password='irCCY7ZZY4zrNyz8',
        database='ai-mysticism'
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
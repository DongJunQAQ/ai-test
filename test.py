import psycopg2

db = psycopg2.connect(host='192.168.246.188', user='postgres', password='123456', port=5432, dbname='postgres')
cursor = db.cursor()  # 获取数据库操作游标
# 插入数据
data = {
    'id': '001',
    'name': 'dongjun',
    'age': 22
}
table = "students"
keys = ','.join(data.keys())  # 使用逗号连接可迭代的元素，id,name,age
vales = ','.join(['%s'] * len(data))  # %s,%s,%s
insert_data_sql = f'INSERT INTO {table}({keys}) VALUES({vales})'  # 动态插入SQL语句
try:
    cursor.execute(insert_data_sql, tuple(data.values()))  # 执行插入操作
    db.commit()  # 插入、更新、删除都需要调用此方法才能生效
    print("插入成功")
except Exception:
    db.rollback()  # 如果执行失败则数据回滚
    print("插入失败，数据回滚")
db.close()

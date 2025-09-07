import sqlite3


def create_connection(db_file):
    """创建数据库连接"""
    conn = sqlite3.connect(db_file)
    print(f"成功连接到SQLite数据库，版本：{sqlite3.version}")
    return conn


def create_table(conn, create_table_sql):
    """根据SQL语句创建表"""
    c = conn.cursor()  # 获取数据库链接的游标
    c.execute(create_table_sql)


def insert_data(conn, data):
    """插入数据"""
    sql = '''INSERT INTO students(name, age, email) VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()  # 提交事务
    return cur.lastrowid  # 返回最后插入数据的ID


def select_all_data(conn):
    """查询所有数据"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()  # 获取所有结果
    return rows


def select_data_by_age(conn, age):
    """按条件查询数据"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE age >= ?", (age,))
    rows = cur.fetchall()
    return rows


def update_data(conn, rows_id, new_age):
    """更新数据"""
    sql = '''UPDATE students SET age = ? WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (new_age, rows_id))
    conn.commit()


def delete_data(conn, rows_id):
    """删除数据"""
    sql = 'DELETE FROM students WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (rows_id,))
    conn.commit()


if __name__ == "__main__":
    database = "example.db"  # 数据库文件名，如果该文件不存在则自动创建
    create_students_table_sql = """CREATE TABLE IF NOT EXISTS students (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            age integer,
                                            email text
                                        );"""
    # 连接数据库
    connection = create_connection(database)
    if connection:
        # 创建表
        create_table(connection, create_students_table_sql)
        # 插入数据
        student1 = ("张三", 20, "zhangsan@example.com")
        student_id = insert_data(connection, student1)
        print(f"\n最后插入的学生的ID: {student_id}")
        # 查询所有数据
        print("\n所有学生:")
        for row in select_all_data(connection):
            print(row)
        # 按条件查询数据
        print("\n年龄大于等于20的学生:")
        for row in select_data_by_age(connection, 20):
            print(row)
        # 更新数据
        update_data(connection, 1, 18)
        # 删除数据
        delete_data(connection, 4)
        # 关闭连接
        connection.close()

from component import mymysql
from component.mymysql import execute

mymysql.init({
    'host': "192.168.121.133",
    'port': 3306,
    'database': 'laashub',
    'user': 'laashub',
    'password': 'laashub123',
    'charset': 'utf8mb4',
})

if __name__ == '__main__':
    target_id = 38
    # query all
    print(execute("""
    select * from designer_data_directory
    """))
    # query with condition
    print(execute("""
    select * from designer_data_directory where id = %(id)s
    """, {
        "id": target_id
    }))
    # insert
    print(execute("""
        insert into designer_data_directory(pid, name) values (%(pid)s,%(name)s)
        """, {
        "pid": target_id,
        "name": "test2"
    }))
    # update
    print(execute("""
        update designer_data_directory set name = %(name)s where id = %(id)s
        """, {
        "id": target_id,
        "name": "test",
    }))
    # delete
    print(execute("""
            delete from designer_data_directory where id = %(id)s
            """, {"id": target_id}))

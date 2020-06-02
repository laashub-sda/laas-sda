import json

from flask import Blueprint

from ...component import form
from ...component import mymysql
from ...exception import MyServiceException

app = Blueprint('distribution_data_directory', __name__,
                url_prefix='/distribution/data/directory')


@app.route('/select', methods=['POST'])
def select():
    request_data = form.check()
    select_sql_keys = "id, pid, name"
    select_sql_where = ''
    params = {}
    if request_data.__contains__('id'):
        select_sql_keys += ', description'
        select_sql_where = " and id = %(id)s "
        params['id'] = request_data["id"]
    select_sql = 'select ' + select_sql_keys + ' from designer_data_directory where 1 = 1 ' + select_sql_where
    return json.dumps(mymysql.execute(select_sql, params))


@app.route('/insert', methods=['POST'])
def insert():
    request_data = form.check(["pid", "name"])
    pid = request_data["pid"]
    name = request_data["name"]

    insert_result = mymysql.execute("""
            insert into designer_data_directory(pid, name) values (%(pid)s, %(name)s)
        """, {
        "pid": pid,
        "name": name,
    })

    json.dumps(mymysql.execute("""
                CREATE TABLE designer_data_data_%(id)s (
                    id int(11) NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """, {
        "id": insert_result,
    }))

    return json.dumps(insert_result)


@app.route('/update', methods=['POST'])
def update():
    request_data = form.check(["id"])

    params = {}
    update_set_sql_str = ""

    params["id"] = request_data["id"]

    if request_data.__contains__("name"):
        params["name"] = request_data["name"]
        update_set_sql_str = "name=%(name)s, "

    if request_data.__contains__("pid"):
        params["pid"] = request_data["pid"]
        update_set_sql_str = "pid=%(pid)s, "

    if request_data.__contains__("description"):
        params["description"] = request_data["description"]
        update_set_sql_str = "description=%(description)s, "

    if "" == update_set_sql_str:
        raise MyServiceException("no content for update set")

    update_set_sql_str = update_set_sql_str[:len(update_set_sql_str) - 2]

    return json.dumps(
        mymysql.execute("update designer_data_directory set " + update_set_sql_str + " where id = %(id)s", params))


@app.route('/delete', methods=['POST'])
def delete():
    request_data = form.check(["id"])

    def get_children(_id):
        return mymysql.execute("""
            select id
            from designer_data_directory
            where pid = %(id)s
            """, {"id": _id})

    def delete_one_level(_id):
        # drop table designer_data_data_
        mymysql.execute("""
                    drop table designer_data_data_%(id)s
                    """, {"id": _id})
        return mymysql.execute("""
            delete
            from designer_data_directory
            where id = %(id)s
            """, {"id": _id})

    def do_delete(_id):
        children = get_children(_id)
        if len(children) > 0:
            for item in children:
                do_delete(item["id"])
        delete_one_level(_id)

    do_delete(request_data["id"])
    return ""


@app.route('/fork', methods=['POST'])
def fork():
    pass

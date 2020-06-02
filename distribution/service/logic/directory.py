import json

from flask import Blueprint

from ...component import form
from ...component import mymysql
from ...exception import MyServiceException

app = Blueprint('distribution_logic_directory', __name__,
                url_prefix='/distribution/logic/directory')


@app.route('/select', methods=['POST'])
def select():
    return json.dumps(mymysql.execute("""
        select id, pid, name, description
        from designer_logic_directory
    """, {

    }))


@app.route('/insert', methods=['POST'])
def insert():
    request_data = form.check(["pid", "name"])
    pid = request_data["pid"]
    name = request_data["name"]

    insert_result = mymysql.execute("""
        insert into designer_logic_directory(pid, name) values (%(pid)s, %(name)s)
    """, {
        "pid": pid,
        "name": name,
    })

    # insert logic_data
    mymysql.execute("""
            insert into designer_logic_data(did, file) values (%(did)s, %(file)s)
        """, {
        "did": insert_result,
        "file": '',
    })

    return json.dumps(insert_result)


@app.route('/update', methods=['POST'])
def update():
    request_data = form.check(["id"])
    params = {}
    update_set_sql_str = ""

    params["id"] = request_data["id"]

    if request_data.__contains__("name"):
        params["name"] = request_data["name"]
        update_set_sql_str = "set name=%(name)s"

    if request_data.__contains__("pid"):
        params["pid"] = request_data["pid"]
        update_set_sql_str = "set pid=%(pid)s"

    if "" == update_set_sql_str:
        raise MyServiceException("no content for update set")

    return json.dumps(
        mymysql.execute("update designer_data_directory " + update_set_sql_str + " where id = %(id)s", params))


@app.route('/delete', methods=['POST'])
def delete():
    request_data = form.check(["id"])

    def get_children(_id):
        return mymysql.execute("""
            select id
            from designer_logic_directory
            where pid = %(id)s
            """, {"id": _id})

    def delete_one_level(_id):
        # delete logic data
        mymysql.execute("""
                    delete from designer_logic_data where did = %(did)s
                    """, {"did": _id})

        return mymysql.execute("""
            delete
            from designer_logic_directory
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

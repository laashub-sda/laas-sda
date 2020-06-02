import json

from flask import Blueprint

from ...component import form
from ...component import mymysql

app = Blueprint('distribution_logic_data', __name__,
                url_prefix='/distribution/logic/data')


@app.route('/select', methods=['POST'])
def select():
    request_data = form.check(["did"])
    return json.dumps(mymysql.execute("""
        select id, file
        from designer_logic_data
        where did = %(did)s
    """, request_data))


@app.route('/update', methods=['POST'])
def update():
    request_data = form.check(["id", "file"])
    update_designer_data_logic_associate(request_data['id'], request_data['file'])
    return json.dumps(mymysql.execute("""
        update designer_logic_data
        set file = %(file)s
        where id = %(id)s
    """, request_data))


def update_designer_data_logic_associate(logic_id, file):
    # clear old data
    logic_data = {'logic_id': logic_id}
    mymysql.execute('delete from designer_data_logic_io where logic_id = %(logic_id)s', logic_data)
    mymysql.execute('delete from designer_data_logic_trigger where logic_id = %(logic_id)s', logic_data)
    # parse data content
    start_data_define_str = '# start data_define'
    end_data_define_str = '# end data_define'
    data_logic_associate_obj = eval(
        file[file.find(start_data_define_str) + len(start_data_define_str):file.find(end_data_define_str)])

    def insert_data_logic_io(service_type, logic_id, values):
        if not values and len(values) < 1:
            return
        sql = 'insert into designer_data_logic_io(data_id, logic_id, type) values'
        sql_value = {
            'logic_id': logic_id,
            'type': service_type,
        }
        # loop every value
        for value in values:
            sql += '(%(data_id_' + value + ')s, %(logic_id)s, %(type)s), '
            sql_value['data_id_' + value] = value
        sql = sql[:len(sql) - 2]
        # execute sql
        mymysql.execute(sql, sql_value)

    insert_data_logic_io('get', logic_id, data_logic_associate_obj['get'])
    insert_data_logic_io('set', logic_id, data_logic_associate_obj['set'])

    # trigger
    def insert_data_logic_io_trigger(logic_id, trigger_value):
        if not trigger_value and trigger_value.keys() < 1:
            return
        sql = 'insert into designer_data_logic_trigger(data_id, logic_id, func_name, type) values'
        sql_value = {
            'logic_id': logic_id,
        }
        for data_key in trigger_value:
            data_level = trigger_value[data_key]
            for event_key in data_level:
                event_level = data_level[event_key]
                data_event = data_key + "_" + event_key
                sql += "(%(data_id_" + data_event + ")s, %(logic_id)s, %(func_name_" + data_event \
                       + ")s, %(type_" + data_event + ")s), "
                sql_value["data_id_" + data_event] = data_key
                sql_value["type_" + data_event] = event_key
                sql_value["func_name_" + data_event] = event_level
        sql = sql[:len(sql) - 2]
        mymysql.execute(sql, sql_value)

    insert_data_logic_io_trigger(logic_id, data_logic_associate_obj["trigger"])
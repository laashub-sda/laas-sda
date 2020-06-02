import json

from flask import Blueprint

from ...component import form
from ...component import mymysql

app = Blueprint('distribution_data_logic_trigger', __name__,
                url_prefix='/distribution/data_logic/trigger')


@app.route('/select', methods=['POST'])
def select():
    request_data = form.check(['data_id'])
    return json.dumps(
        mymysql.execute(
            'select data_id, logic_id, func_name, type from designer_data_logic_trigger where data_id = %(data_id)s',
            request_data))


@app.route('/select_batch_status', methods=['POST'])
def select_batch_status():
    request_data = form.check(['data_data_data_id_list_str'])
    data_data_data_id_list_str = request_data['data_data_data_id_list_str']
    sql = """
                    select t1.status, t1.data_event_type, t1.data_data_id
                    from(
                        select max(id) as id, concat(data_id,'_',data_data_id) as data_data_data_id
                        from engine_data_logic_trigger_data_status
                        group by data_id, data_data_id
                    )t, engine_data_logic_trigger_data_status t1
                    where t.data_data_data_id in (%s)
                    and t.id = t1.id
            """ % data_data_data_id_list_str
    query_result = mymysql.execute(sql, request_data)
    return json.dumps(query_result)

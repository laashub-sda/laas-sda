import json

from flask import Blueprint

from . import struct
from ...component import form
from ...component import mymysql

app = Blueprint('distribution_data_data', __name__,
                url_prefix='/distribution/data/data')

"""
request_standard = {
    'page_current': -1,
    'page_size': 10,
    'search': {},
    'order': [],
}
resp_standard = {
    'page_total': 10,
    'data': [],

    'page_current': -1,
    'page_size': 10,
    'search': {},
    'order': [],
}
"""


@app.route('/select', methods=['POST'])
def select():
    request_data = form.check(['search'])
    search = request_data['search']
    did = search['did']
    if request_data.__contains__('page_current'):
        page_current = request_data['page_current']
        if page_current < 1:
            page_current = 1
    else:
        page_current = 1
    if request_data.__contains__('page_size'):
        page_size = request_data['page_size']
    else:
        page_size = 10
    if request_data.__contains__('search'):
        search = request_data['search']
    else:
        search = {}
    if request_data.__contains__('order'):
        order = request_data['order']
    else:
        order = []

    designer_data_data_table_name = 'designer_data_data_' + str(did)
    select_value = {}
    # where
    select_sql_where = ''
    for item in search:
        select_value[item] = search[item]
        if 'did' == item:
            continue
        select_sql_where += ' and ' + item + ' = %(' + item + ')s'
        select_value[item] = search[item]

    # page
    page_total = mymysql.execute(
        'select count(1) as page_total from ' + designer_data_data_table_name + ' where 1 = 1 ' + select_sql_where,
        select_value)
    page_total = page_total[0]['page_total']
    select_sql_page = " LIMIT " + str(((page_current - 1) * page_size)) + ", " + str(page_size)

    select_sql_keys = 'id, '
    # got the data table' column
    data_struct_list = mymysql.execute('select code from designer_data_struct where did = %(did)s', {'did': did})
    for item in data_struct_list:
        data_data_table_column = item['code']
        select_sql_keys += data_data_table_column + ', '
    select_sql_keys = select_sql_keys[:len(select_sql_keys) - 2]

    # data
    select_sql = 'select ' + select_sql_keys + ' from ' + designer_data_data_table_name + ' where 1 = 1 ' \
                 + select_sql_where + select_sql_page
    data = mymysql.execute(select_sql, select_value)
    #
    return json.dumps({
        'page_total': page_total,
        'data': data,
        'page_current': page_current,
        'page_size': page_size,
        'search': search,
        'order': order,
    })


@app.route('/insert', methods=['POST'])
def insert():
    request_data = form.check(['did'])
    did = request_data['did']
    designer_data_data_table_name = 'designer_data_data_' + str(did)
    insert_sql_keys = ''
    insert_sql_values = ''
    # got the data table' column
    data_struct_list = json.loads(struct.select())
    for item in data_struct_list:
        data_data_table_column = item['code']
        if request_data.__contains__(data_data_table_column):
            insert_sql_keys += data_data_table_column + ', '
            insert_sql_values += '%(' + data_data_table_column + ')s, '
    insert_sql_keys = insert_sql_keys[:len(insert_sql_keys) - 2]
    insert_sql_values = insert_sql_values[:len(insert_sql_values) - 2]

    return json.dumps(mymysql.execute(
        'insert into ' + designer_data_data_table_name + '(' + insert_sql_keys + ') values(' + insert_sql_values + ')',
        json.loads(json.dumps(request_data))))


@app.route('/update', methods=['POST'])
def update():
    request_data = form.check(['did', 'id'])
    did = request_data['did']
    designer_data_data_table_name = 'designer_data_data_' + str(did)
    update_sql = ''
    # got the data table' column
    data_struct_list = json.loads(struct.select())
    for item in data_struct_list:
        data_data_table_column = item['code']
        if 'id' == data_data_table_column:
            continue
        if request_data.__contains__(data_data_table_column):
            update_sql += data_data_table_column + ' = ' + '%(' + data_data_table_column + ')s, '
    update_sql = update_sql[:len(update_sql) - 2]

    return json.dumps(mymysql.execute(
        'update ' + designer_data_data_table_name + ' set ' + update_sql + ' where id = %(id)s ',
        request_data))


@app.route('/delete', methods=['POST'])
def delete():
    request_data = form.check(['did', 'id'])
    did = request_data['did']
    designer_data_data_table_name = 'designer_data_data_' + str(did)

    return json.dumps(mymysql.execute(
        'delete from ' + designer_data_data_table_name + ' where id = %(id)s ',
        request_data))

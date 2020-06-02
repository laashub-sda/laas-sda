import json

from flask import Blueprint

from ...component import form
from ...component import mymysql

app = Blueprint('distribution_data_logic_io', __name__,
                url_prefix='/distribution/data_logic/io')


@app.route('/select', methods=['POST'])
def select():
    request_data = form.check(['data_id'])
    return json.dumps(
        mymysql.execute('select data_id, logic_id, type from designer_data_logic_io where data_id = %(data_id)s',
                        request_data))

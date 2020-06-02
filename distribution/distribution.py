import json

from flask import Blueprint, request, make_response

from .component import mymysql
from .exception import MyServiceException

app = Blueprint('distribution_distribution', __name__,
                url_prefix='/distribution/distribution')


@app.route('/data', methods=['POST'])
def data():
    try:
        request_data = json.loads(request.get_data())
        if not request_data.__contains__("sql"):
            raise MyServiceException("missing param: sql")
        sql = request_data["sql"]
        if request_data.__contains__("parameters"):
            parameters = request_data["parameters"]
        else:
            parameters = {}
        print("distribution/distribution: ", "sql: ", sql, "parameters: ", str(parameters))
        execute_result = mymysql.execute(sql, parameters)
        return json.dumps(execute_result)
    except MyServiceException as e:
        print("e.msg: ", e.msg)
        custom_res = make_response(e.msg)
        custom_res.status = "500"
        return custom_res

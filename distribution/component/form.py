import json

from flask import request

from ..exception import MyServiceException


def check(check_data_keys=[]):
    request_data = json.loads(request.get_data())
    if check_data_keys and len(check_data_keys) > 0:
        for item in check_data_keys:
            if not request_data.__contains__(item):
                raise MyServiceException("missing param: %s" % item)
    return request_data

import axios from "axios";

async function select_(data_struct) {
  let net_request_result = await axios.post("/distribution/logic/data/select", data_struct);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}


async function update_(data_struct) {
  let net_request_result = await axios.post("/distribution/logic/data/update", data_struct);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}


function get_standard_content() {
  return `from engine import Data
from engine import Runtime

Runtime.define_dependencies(["dingtalkchatbot"])


def test(engine_data):
    data_id = engine_data["data_id"]
    data_data_id = engine_data["data_data_id"]
    data_event_type = engine_data["data_event_type"]
    logic_id = engine_data["logic_id"]
    func_name = engine_data["func_name"]
    print("test")
    json = Runtime.require('json')
    print("json: ", json)
    print("data_id: ", data_id, "data_data_id: ", data_data_id, "data_event_type: ", data_event_type, "logic_id: ",logic_id, "func_name: ", func_name)
    sql_result = Data.get(' select * from designer_data_data_%(data_id)s where id=%(data_data_id)s ', {'data_id': data_id, 'data_data_id': data_data_id})
    print(str(sql_result))
    # Data.get(' select username, password from aliyun ')
    # Data.set(' insert into aliyun(username, password) values(%(username)s, %(password)s) ', {'username': 'xxx', 'password': 'xxx'})
    # Data.set(' update host set password where id = %(id)s ', {'id': '1'})
    # Data.set(' delete from aliyun where username = %(username)s ', {'username': 'xxx'})


# start data_define
{
    'get': [
        '21',
    ],
    'set': [
        '21',
    ],
    'trigger': {
        '21': {
            'insert': 'test'
        },
    }
}
#  end data_define

`;
}

export default {
  get_standard_content,
  select_,
  update_,
}

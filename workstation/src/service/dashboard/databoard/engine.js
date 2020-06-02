import axios from "axios";


async function trigger(request_data) {
  let net_request_result = await axios.post("/engine/engine/trigger", request_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

async function select_engine_data_logic_trigger_status_details_status(request_data) {
  let net_request_result = await axios.post("/engine/engine/select_engine_data_logic_trigger_status_details_status", request_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

async function select_engine_data_logic_trigger_status_details_log(request_data) {
  let net_request_result = await axios.post("/engine/engine/select_engine_data_logic_trigger_status_details_log", request_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

export default {
  trigger,
  select_engine_data_logic_trigger_status_details_status,
  select_engine_data_logic_trigger_status_details_log,
}

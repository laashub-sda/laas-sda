import axios from "axios";

async function select_(data_id) {
  let net_request_result = await axios.post("/distribution/data_logic/io/select", data_id);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

export default {
  select_
}

import axios from "axios";

async function select_(data_data) {
  let net_request_result = await axios.post("/distribution/data/data/select", data_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

async function insert_(data_data) {
  let net_request_result = await axios.post("/distribution/data/data/insert", data_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

async function update_(data_data) {
  let net_request_result = await axios.post("/distribution/data/data/update", data_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

async function delete_(data_data) {
  let net_request_result = await axios.post("/distribution/data/data/delete", data_data);
  if (!net_request_result || !net_request_result.status || net_request_result.status != 200 || !net_request_result.data) return;
  return net_request_result.data;
}

export default {
  select_,
  insert_,
  update_,
  delete_,

}

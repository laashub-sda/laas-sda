const nav_area_width_designer = 10;
const nav_area_width_use = 43;
const table_column_operation_status_width = 130;
const editable_table_common_operation_column_width = 90;

function cancel_opt_data(component) {
  const opt_name = component._data.opt_name;
  if ("insert" == opt_name) {
    component._data.data.pop();
  } else if ("update" == opt_name) {
    // 还原
    component._data.is_in_opt = false;
    component._data.opt_name = "";
    const cur_line = component._data.opt_line;
    component._data.opt_line = -1;
    component._data.data[cur_line] = component._data.data_line_backup;
  }
  component._data.is_in_opt = false;
  component._data.opt_name = "";
  component._data.opt_line = -1;
}

function calculate_table_column_width(is_in_designer, component, column_number) {
  const window_width = document.documentElement.clientWidth;
  const right_window_width = window_width * (1 - component.split);
  let nav_area_width = nav_area_width_designer;
  let table_column_operation_status_width_temp = 0;
  if (!is_in_designer) {
    nav_area_width = nav_area_width_use;
  } else {
    table_column_operation_status_width_temp = table_column_operation_status_width;
  }
  return (right_window_width - editable_table_common_operation_column_width - table_column_operation_status_width_temp - nav_area_width) / column_number;
}

function editable_table_common_column(component, title, key, column_width) {
  return {
    title: title,
    key: key,
    sortable: true,
    width: column_width,
    // fixed: 'left',
    align: 'center',
    titleHtml: ' <i class="ivu-icon ivu-icon-edit"></i>',
    editable: true,
    resizable: true,
    render: function (h, params) {
      // is in edit status
      if (component._data.is_in_opt && component._data.opt_line == params.index) {
        let edit_value = "";
        if ("insert" == component._data.opt_name) {
        } else if ("update" == component._data.opt_name) {
          edit_value = component._data.data[params.index][params.column.key];
        }
        return h('Input', {
          props: {
            type: 'text',
            value: edit_value
          },
          on: {
            'on-change'(event) {
              component._data.data[params.index][params.column.key] = event.target.value;
            }
          }
        })
      }
      return h('div', {
        domProps: {
          innerHTML: component._data.data[params.index][params.column.key],
        },
      })
    }
  }
}


function editable_table_common_operation_column(component) {
  return {
    title: 'operation',
    slot: 'operation',
    align: 'center',
    width: editable_table_common_operation_column_width,
    resizable: true,
    render: (h, params) => {
      const div_data = [];
      if (component._data.is_in_opt && component._data.opt_line == params.index) {
        div_data.push(h('Button', {
          props: {
            type: 'primary',
            size: 'small'
          },
          style: {
            marginRight: '10px',
            marginTop: '10px',
            marginBottom: '10px',
          },
          on: {
            click: () => {
              const cur_line_index = params.index;
              const cur_line_data = component._data.data[cur_line_index];
              cancel_opt_data(component, cur_line_data);
            }
          }
        }, 'cancel'));
        div_data.push(h('Button', {
          props: {
            type: 'error',
            size: 'small'
          },
          style: {
            marginRight: '10px',
            marginTop: '10px',
            marginBottom: '10px',
          },
          on: {
            click: () => {
              const cur_line_index = params.index;
              const cur_line_data = component._data.data[cur_line_index];
              cur_line_data['did'] = component.directory_id;

              if ("insert" == component._data.opt_name) {
                component.insert_(component, cur_line_data);
              } else if ("update" == component._data.opt_name) {
                component.update_(component, cur_line_data);
              }
            }
          }
        }, 'save'));
      }
      let is_display_edit = true;
      if (component._data.is_in_opt && component._data.opt_line == params.index && ("update" == component._data.opt_name || "insert" == component._data.opt_name)) {
        is_display_edit = false;
      }
      if (is_display_edit) {
        div_data.push(h('Button', {
          props: {
            type: 'error',
            size: 'small'
          },
          style: {
            marginRight: '10px',
            marginTop: '10px',
            marginBottom: '10px',
          },
          on: {
            click: () => {
              const cur_line_index = params.index;
              component._data.is_in_opt = true;
              component._data.opt_name = "update";
              component._data.opt_line = cur_line_index;
              const cur_line_data = component._data.data[cur_line_index];
              component._data.data[cur_line_index] = cur_line_data;
              cur_line_data['did'] = component.directory_id;
              component._data.data_line_backup = JSON.parse(JSON.stringify(cur_line_data));
            }
          }
        }, 'edit'));
      }
      if (is_display_edit) {
        div_data.push(h('Button', {
          props: {
            type: 'error',
            size: 'small'
          },
          style: {
            marginRight: '10px',
            marginTop: '10px',
            marginBottom: '10px',
          },
          on: {
            click: () => {
              component.$Modal.warning({
                title: "tips",
                content: "are you ready to delete?",
                okText: "YES",
                onOk: function () {
                  const cur_line_index = params.index;
                  component._data.is_in_opt = true;
                  component._data.opt_name = "delete";
                  component._data.opt_line = cur_line_index;
                  const cur_line_data = component._data.data[cur_line_index];
                  cur_line_data['did'] = component.directory_id;

                  component.delete_(component, cur_line_data);
                },
                closable: true,
                onCancel: function () {

                },
                cancelText: ""
              });

            }
          }
        }, 'delete'));
      }
      return h('div', div_data);
    }
  };
}


function table_column_operation_status(component) {
  return {
    title: 'operation-status',
    slot: 'operation-status',
    align: 'center',
    width: table_column_operation_status_width,
    resizable: true,
    render: (h, params) => {
      if (component._data.is_in_opt) return [];
      const div_data = [];
      // event_type:current_status
      const data_status_data = component.data_status[params.index];
      if (!data_status_data) return [];
      const data_status = data_status_data["status"];
      let primary_str = "info";
      if ("FINISH" == data_status) {
        primary_str = "success";
      } else {
        primary_str = "error";
      }
      div_data.push(h('Button', {
        props: {
          type: primary_str,
          size: 'small'
        },
        style: {
          marginRight: '10px',
          marginTop: '10px',
          marginBottom: '10px',
        },
      }, data_status_data["data_event_type"] + ":" + data_status));
      // Details
      div_data.push(h('Button', {
        props: {
          type: 'primary',
          size: 'small'
        },
        style: {
          marginRight: '10px',
          marginTop: '10px',
          marginBottom: '10px',
        },
        on: {
          click: async () => {
            // gen data status details tree data
            component.data_status_details.display = true;
            const data_data_id = component.data[params.index]["id"];
            await component.select_engine_data_logic_trigger_status_details_status(component,data_data_id);
            await component.select_engine_data_logic_trigger_status_details_log(component, "tree", {"data_data_id": data_data_id});
          }
        }
      }, 'Details'));
      // Pause
      // Resume
      // Delay
      // GiveUp
      // TODO improvement: support the Pause/Resume/Delay/GiveUp operation
      return h('div', div_data);
    }
  };
}

function init_insert_(component) {
  // can not continuous multiple times add/update
  if (component._data.is_in_opt) {
    component.$Message.error("can not continuous multiple times add/update");
    return;
  }
  component._data.is_in_opt = true;
  component._data.opt_name = "insert";

  // construct column
  const temp_data_one = {};
  for (const item of component._data.columns) {
    const key = item["key"];
    if (key && key != "") {
      temp_data_one[key] = "";
    }
  }
  component._data.opt_line = component._data.data.length;
  component._data.data.push(temp_data_one);
}


// TODO improvement: memory table column width for open again
// TODO improvement: lock button on table column, click it can make the column fix to left
export default {
  table_column_operation_status,
  editable_table_common_operation_column,
  editable_table_common_column,
  calculate_table_column_width,
  cancel_opt_data,
  init_insert_,
}

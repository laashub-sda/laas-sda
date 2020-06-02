<template>
  <div>
    <DirectoryDescription :directory_id="directory_id"></DirectoryDescription>
    <!--    <Button @click="init_table">Refresh</Button>-->

    <i-button @click="init_table">SEARCH</i-button>
    <i-button @click="init_insert_">ADD</i-button>

    <!--search area-->
    <divider orientation="left" style="font-size: 12px;">
      <i-button
        @click="function(){search.expand_status=!search.expand_status;}">
        EXPAND/COLLAPSE SEARCH CONDITION AREA
      </i-button>
    </divider>
    <div v-if="search.expand_status" style="margin-left: 10px">
      <!--dynamic search form-->
      <i-form :model="search.data"
              :label-width="80">
        <row>
          <i-col span="6" v-for="item in search.template">
            <form-item :label="item.label" :prop="item.prop">
              <i-input v-model="item.v_model"></i-input>
            </form-item>
          </i-col>
        </row>
      </i-form>
    </div>
    <!--operator-->
    <!--                                        <div style="margin-left: 10px;margin-bottom: 10px">-->
    <!--                                            <i-button >test</i-button>-->
    <!--                                        </div>-->
    <i-table stripe border :columns="columns"
             :data="data"
             :loading="loading"
             height="690"
             border
    ></i-table>
    <!--data status show detail modal-->
    <modal v-model="data_status_details.display" width="100vw">
      <p slot="header">
        <span>details</span>
      </p>
      <div>
        <row>
          <i-col span="6">
            <vue-tree-list
              @click="onClickEngineDataLogicDetailStatusTree"
              :model="data_status_details_tree"
              default-tree-node-name="new"
              default-leaf-node-name="new"
              v-bind:default-expanded="true">
              <span class="icon" slot="addTreeNodeIcon"></span>
              <span class="icon" slot="addLeafNodeIcon"></span>
              <span class="icon" slot="editNodeIcon"></span>
              <span class="icon" slot="delNodeIcon"></span>
              <span class="icon" slot="leafNodeIcon"></span>
              <span class="icon" slot="treeNodeIcon"></span>
            </vue-tree-list>

            <!--@on-select-change="load_target_time_log"-->
          </i-col>
          <i-col span="18" style="background: #2b2b2b;color: white">
                                                        <pre v-for="item in data_status_details.log_list">
                                                            {{item}}
                                                        </pre>
          </i-col>
        </row>
      </div>
      <div slot="footer"></div>
    </modal>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <page show-sizer :total="page.total" :current="1"
              @on-change="function(current){page.current = current;init_table();}"
              @on-page-size-change="function(page_size){page.page_size = page_size;init_table();}"
        />
      </div>
    </div>

  </div>
</template>

<script>
    import {Tree, VueTreeList} from 'vue-tree-list'
    import DirectoryDescription from "../../../component/directory/DirectoryDescription";
    import designer_data_struct from "../../designer/designer_data/designer_data_struct/designer_data_struct";
    import designer_data_data from "./data_board_data";
    import component_table from "../../../component/table";
    import designer_data_logic_trigger from "../../designer/designer_data_logic_trigger";
    import engine from "./engine";

    const update_description_btn_str = "update description";
    const save_description_btn_str = "save description";


    export default {
        name: "DesignerDataData",
        props: {
            directory_id: {
                default: 60,
                type: Number,
            },
            directory_name: {
                default: 'test',
                type: String,
            },
            split_value: {
                default: 0.2,
            },
        },
        components: {
            DirectoryDescription,
            VueTreeList,
        },
        data() {
            return {
                column_keys: [],
                columns: [],
                data: [],
                data_status: [],
                data_status_details_tree: new Tree([]),
                data_status_details: {
                    display: false,
                    log_list: [],
                },
                data_line_backup: {},
                loading: false,
                is_in_opt: false,
                opt_name: "",
                opt_line: -1,
                page: {
                    current: 1,
                    total: 0,
                    page_size: 10
                },
                search: {
                    expand_status: false,
                    data: {},
                    template: [],
                },
                associate: {
                    trigger: {
                        "insert": [],
                        "update": [],
                        "delete": [],
                    },
                },
                data_event_2_logic: {
                    cur_choose: {
                        value: [],
                        logic_id: '',
                        func_name: '',
                    },
                    data: [],
                },
            }
        },
        methods: {
            async init_table_column() {
                await component_table.cancel_opt_data(this);
                this._data.loading = true;
                try {
                    const data_struct_list = await designer_data_struct.select_({'did': this.directory_id});
                    if (data_struct_list < 1) {
                        this._data.loading = false;
                        return;
                    }
                    const column_width = component_table.calculate_table_column_width(false, this, data_struct_list.length);
                    // basic column
                    for (const item of data_struct_list) {
                        const code = item["code"];
                        const meaning = item["meaning"];
                        this._data.column_keys.push(code);
                        this._data.columns.push(component_table.editable_table_common_column(this, meaning, code, column_width));
                        this._data.search.template.push({"label": meaning, "prop": code, "v_model": ""});
                    }
                    // operation column
                    this._data.columns.push(component_table.editable_table_common_operation_column(this));

                    this.$Message.success('query data data columns success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
                this._data.loading = false;
            },
            async init_table() {
                await component_table.cancel_opt_data(this);
                this._data.loading = true;
                try {
                    /*                    const request_standard = {
                                            page_current: -1,
                                            page_size: 10,
                                            search: {},
                                            order: [],
                                        }
                                        const resp_standard = {
                                            page_total: 10,
                                            data: [],

                                            page_current: -1,
                                            page_size: 10,
                                            search: {},
                                            order: [],
                                        }*/
                    // page & search (order,search with express)
                    const request_data = {
                        page_current: this._data.page.current,
                        page_size: this._data.page.page_size,
                        search: {'did': this.directory_id},
                    };
                    // gen search
                    const search_list = this._data.search.template;
                    for (const item of search_list) {
                        const prop = item["prop"];
                        const v_model = item["v_model"];
                        if (!v_model || v_model == '') continue;
                        request_data.search[prop] = v_model;
                    }
                    const resp_data = await designer_data_data.select_(request_data);
                    this._data.page.total = resp_data['page_total'];
                    this._data.data = resp_data['data'];
                    this.$Message.success('query data_struct success');
                    await this.init_data_logic_trigger_status();
                    // status column
                    if (this._data.columns.length < this._data.column_keys.length + 2)
                        this._data.columns.push(component_table.table_column_operation_status(this));
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                } finally {
                    this._data.loading = false;
                }
            },
            async init_associate() {
                // trigger
                const designer_data_logic_trigger_list = await designer_data_logic_trigger.select_({'data_id': this.directory_id});
                for (const item of designer_data_logic_trigger_list) {
                    this._data.associate.trigger[item["type"]].push(item["logic_id"] + ":" + item["func_name"]);
                }
            },
            async init_data_logic_trigger_status() {
                if (!this._data.data || this._data.data.length < 1) return;
                const data_id = this.directory_id;
                let data_data_data_id_list_str = "";
                for (const item of this._data.data) {
                    const data_data_id = item["id"];
                    data_data_data_id_list_str += "'" + data_id + "_" + data_data_id + "', ";
                }
                data_data_data_id_list_str = data_data_data_id_list_str.substring(0, data_data_data_id_list_str.length - 2);
                try {
                    let net_request_result = await designer_data_logic_trigger.select_batch_status({"data_data_data_id_list_str": data_data_data_id_list_str});
                    this._data.data_status = net_request_result;
                    this.$Message.success('query data logic trigger success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
            },
            init_insert_() {
                component_table.init_insert_(this);
            },
            async insert_(component, data_data) {
                try {
                    if (!await this.associate_data_logic_event(component, data_data, 'insert')) return;
                    const insert_result = await designer_data_data.insert_(data_data);
                    component.$Message.success('insert data data success');
                    await component.trigger_engine(component, 'insert', insert_result);
                    await component.init_table();
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async update_(component, data_data) {
                try {
                    if (!await this.associate_data_logic_event(component, data_data, 'update')) return;
                    await designer_data_data.update_(data_data);
                    component.$Message.success('update data data success');
                    await component.trigger_engine(component, 'update', data_data['id']);
                    await component.init_table();
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async delete_(component, data_data) {
                try {
                    if (!await this.associate_data_logic_event(component, data_data, 'delete')) return;
                    await designer_data_data.delete_(data_data);
                    component.$Message.success('delete data data success');
                    await component.trigger_engine(component, 'delete', data_data['id']);
                    await component.init_table();
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async associate_data_logic_event(component, data_data, data_event_type) {
                if (component.associate.trigger[component.opt_name].length < 1) return true; // data event without logic

                component._data.data_event_2_logic.data = [];
                for (const item of component._data.associate.trigger[data_event_type]) {
                    component._data.data_event_2_logic.data.push({
                        "value": item,
                        "label": item,
                    });
                }
                const result = await new Promise(function (resolve, reject) {
                    component.$Modal.confirm({
                        onOk: () => {
                            if (!component._data.data_event_2_logic.cur_choose.value || component._data.data_event_2_logic.cur_choose.value == "") {
                                resolve(false);
                            }
                            resolve(true);
                        },
                        onCancel: () => {
                            resolve(false);
                        },
                        render: (h) => {
                            return h('cascader', {
                                props: {
                                    "mask-closable": false,
                                    value: component._data.data_event_2_logic.cur_choose.value,
                                    data: component._data.data_event_2_logic.data,
                                },
                                on: {
                                    'on-change': function (value, selectedData) {
                                        component._data.data_event_2_logic.cur_choose.value = value;
                                    }
                                },
                            })
                        }
                    })
                });
                if (!result) {
                    component.$Message.error("you must choose and logic_func when the data_event adapter an logic_func");
                }
                return result;

            },
            async trigger_engine(component, type, data_data_id) { // insert, update, delete
                try {
                    const request_data = {
                        "data_id": component.directory_id,
                        "data_data_id": data_data_id,
                        "type": type,
                    };

                    if (!component._data.data_event_2_logic.cur_choose.value || component._data.data_event_2_logic.cur_choose.value.length <= 0) return;
                    const logic_func_name = component._data.data_event_2_logic.cur_choose.value[0];
                    const logic_func_name_arr = logic_func_name.split(":");
                    request_data["logic_id"] = logic_func_name_arr[0];
                    request_data["func_name"] = logic_func_name_arr[1];
                    await engine.trigger(request_data);
                    component.$Message.success('trigger_engine success');
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async select_engine_data_logic_trigger_status_details_status(component, data_data_id) {
                component._data.data_status_details.tree = [];
                try {
                    let net_request_result = await engine.select_engine_data_logic_trigger_status_details_status({
                        'data_id': component.directory_id,
                        'data_data_id': data_data_id,
                    });

                    `
data_event:1(1):insert:(time)
    logic:1:test:(time)
        START:(time)
        RUNNING:(time)
        FINISH:(time)
        `
                    let last_data_even_type = "";
                    let tree_level_data_event;
                    let tree_level_logic_children;
                    // component._data.data_status_details.tree = new Tree([]);
                    const tree_list = [];
                    let id_temp = 1;
                    while (net_request_result.length > 0) {
                        let item = net_request_result.splice(0, 1)[0];
                        const data_event_type = item["data_event_type"];
                        if (last_data_even_type != data_event_type) {
                            last_data_even_type = data_event_type;
                            tree_level_logic_children = [];
                            if (tree_level_data_event) {
                                tree_list.push(tree_level_data_event);
                            }
                            tree_level_data_event = null;
                        }
                        if (!tree_level_data_event) {
                            tree_level_data_event = {
                                'id': id_temp++,
                                "name": "data_event:{{data_id}}({{data_data_id}}):{{data_event_type}}:({{create_time_str}})".format(item),
                                "tree_level_type": "data_event",
                                "tree_level_data": item,
                                "spread": true,
                                "children": [{
                                    'id': id_temp++,
                                    "name": "logic:{{logic_id}}:{{func_name}}:({{create_time_str}})".format(item),
                                    "tree_level_type": "logic",
                                    "tree_level_data": item,
                                    "spread": true,
                                    "children": tree_level_logic_children,
                                }]
                            };
                        }
                        tree_level_logic_children.push({
                            'id': id_temp++,
                            "name": "{{status}}:({{create_time_str}})".format(item),
                            "tree_level_type": "data_status",
                            "tree_level_data": item,
                        });
                    }
                    tree_list.push(tree_level_data_event);
                    component._data.data_status_details_tree = new Tree(tree_list);
                    component.$Message.success('select engine data logic trigger status details status success');
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async select_engine_data_logic_trigger_status_details_log(component, tree_level_type, tree_level_data) {
                tree_level_data["data_id"] = component.directory_id;
                try {
                    tree_level_data['data_event'] = tree_level_type;
                    const net_request_result = await engine.select_engine_data_logic_trigger_status_details_log(tree_level_data)
                    this._data.data_status_details.log_list = [];
                    for (const item of net_request_result) {
                        this._data.data_status_details.log_list.push(item["log"]);
                    }
                    component.$Message.success('select engine data logic trigger status details log success');
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async onClickEngineDataLogicDetailStatusTree(params) {
                await this.select_engine_data_logic_trigger_status_details_log(this, params.tree_level_type, params.tree_level_data);
            },
        },
        async created() {
            await this.init_associate();
            await this.init_table_column();
            await this.init_table();
        }
    }
    // TODO bug: data operation need more check, there can be only operation at a time
    // TODO improvement: insert/update/delete data operation when across the multi data, so it also need refactor the backend code
</script>

<style scoped>

</style>

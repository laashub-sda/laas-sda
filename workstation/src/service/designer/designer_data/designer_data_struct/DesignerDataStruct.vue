<template>
  <div>
    <DirectoryDescription :directory_id="directory_id"></DirectoryDescription>
    <Button @click="init_table">Refresh</Button>
    <i-button @click="init_insert_">Add</i-button>
    <span style="user-select: text">table_prefix_name: designer_data_data_</span>
    <i-table stripe border :columns="columns"
             :data="data"
             :loading="loading"
    ></i-table>
    <collapse>
      <panel>
        Data Input Channel(Data input from Logic)
        <p slot="content"
           v-for="item in associate.io.set">{{item}}</p>
      </panel>
    </collapse>
    <collapse>
      <panel>
        Data Output Channel(Data output to Logic)
        <p slot="content"
           v-for="item in associate.io.get">{{item}}</p>
      </panel>
    </collapse>
    <!--                                        <collapse>-->
    <!--                                            <panel>-->
    <!--                                                // Data Subscribe Channel(Logic makes the data subscribe to its own changes(running/pause/exception/finish),after the logic changes,it will trigger time to the data,and the data will change)-->
    <!--                                                <p slot="content"-->
    <!--                                                   v-for="item in designer_data_directory.channel.data_subscribe">{{item}}</p>-->
    <!--                                            </panel>-->
    <!--                                        </collapse>-->
    <collapse>
      <panel>
        Data Trigger Channel(Logic subscribe to the data change(crud),after the data chanages, the event will be
        triggered to the logic, and the logic will be executed)
        <div slot="content">
          <!--insert-->
          <collapse>
            <panel>
              insert<p slot="content" v-for="item in associate.trigger.insert">{{item}}</p>
            </panel>
          </collapse>
          <!--update-->
          <collapse>
            <panel>
              update<p slot="content" v-for="item in associate.trigger.update">{{item}}</p>
            </panel>
          </collapse>
          <!--delete-->
          <collapse>
            <panel>
              delete<p slot="content" v-for="item in associate.trigger.delete">{{item}}</p>
            </panel>
          </collapse>

        </div>
      </panel>
    </collapse>

  </div>
</template>

<script>
    import designer_data_struct from "./designer_data_struct";
    import component_table from "../../../../component/table";
    import DirectoryDescription from "../../../../component/directory/DirectoryDescription";
    import designer_data_logic_io from "../../designer_data_logic_io";
    import designer_data_logic_trigger from "../../designer_data_logic_trigger";

    let column_width = component_table.calculate_table_column_width(true, this, 3);

    export default {
        name: "DesignerDataStruct",
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
            DirectoryDescription
        },
        data() {
            return {
                columns: [
                    component_table.editable_table_common_column(this, "code", "code", column_width),
                    component_table.editable_table_common_column(this, "meaning", "meaning", column_width),
                    component_table.editable_table_common_column(this, "reference_type", "reference_type", column_width),
                    component_table.editable_table_common_operation_column(this),
                ],
                data: [],
                data_line_backup: {},
                loading: false,
                is_in_opt: false,
                opt_name: "",
                opt_line: -1,
                associate: {
                    io: {
                        "set": [],
                        "get": [],
                    },
                    trigger: {
                        "insert": [],
                        "update": [],
                        "delete": [],
                    },
                },
                data_event_2_logic: {
                    cur_choose: {
                        value: [],
                        logic_id: "",
                        func_name: "",
                    },
                    data: [],
                },
            }
        },
        methods: {
            async init_table() {
                await component_table.cancel_opt_data(this);
                this._data.loading = true;
                try {
                    this._data.data = await designer_data_struct.select_({'did': this.directory_id});
                    this.$Message.success('query data_struct success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
                this._data.loading = false;
            },
            async init_associate() {
                // io
                const designer_data_logic_io_list = await designer_data_logic_io.select_({'data_id': this.directory_id});
                for (const item of designer_data_logic_io_list) {
                    this._data.associate.io[item["type"]].push(item["logic_id"]);
                }
                // trigger
                const designer_data_logic_trigger_list = await designer_data_logic_trigger.select_({'data_id': this.directory_id});
                for (const item of designer_data_logic_trigger_list) {
                    this._data.associate.trigger[item["type"]].push(item["logic_id"] + ":" + item["func_name"]);
                }
            },
            init_insert_() {
                component_table.init_insert_(this);
            },
            async insert_(component, data_struct) {
                try {
                    await designer_data_struct.insert_(data_struct);
                    component.$Message.success('insert data struct success');
                    await component.init_table();
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async update_(component, data_struct) {
                try {
                    await designer_data_struct.update_(data_struct);
                    component.$Message.success('update data struct success');
                    await component.init_table();
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
            async delete_(component, data_struct) {
                try {
                    await designer_data_struct.delete_(data_struct);
                    component.$Message.success('delete data struct success');
                    await component.init_table();
                } catch (e) {
                    console.log(e.response.data);
                    component.$Message.error(e.response.data);
                }
            },
        },
        async created() {
            await this.init_table();
            await this.init_associate();
        }
    }
    // TODO improvement: increase the multi data_struct flow
</script>

<style scoped>

</style>

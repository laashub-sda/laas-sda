<template>
  <div style="height: 100vh">
    <div>
<!--      <Menu style="font-size: 10px" mode="horizontal" theme="light" :active-name="menu_active_name"-->
<!--            @on-select="function(name){menu_active_name = name}">-->
<!--        <MenuItem :name="item" width="40px" style="user-select:none;text-transform:uppercase;"-->
<!--                  v-for="item in service_type_list">-->
<!--          {{item}}-->
<!--        </MenuItem>-->
<!--      </Menu>-->
      <span>
        <Breadcrumb>
            <BreadcrumbItem v-for="item in breadcrumb.list">
                {{item}}
            </BreadcrumbItem>
        </Breadcrumb>
      </span>
      <span style="margin-left: 30px;font-size: 22px;">
                id: {{directory.cur_id}}
      </span>
    </div>
    <div style="height: 96vh;border: 1px solid #d6d6d6;">
        <span>
            <Split v-model="split">
                <div slot="left">
                  <Directory @click-directory="OnClickDirectory" v-show="menu_active_name==item" :service_type="item"
                             :is_databoard="is_databoard"
                             v-for="item in service_type_list"></Directory>
                </div>
                <div slot="right">
                    <Tabs v-model="tab_pane_cur" type="card"
                          @on-tab-remove="handleTabRemove"
                          @on-click="onClickTab" :animated="false"
                          style="user-select:none;"
                          closable
                          :before-remove='beforeRemove'
                    >

                        <TabPane v-if="item.visible" :label="item.label"
                                 v-for="(item,index) in tab_pane"
                                 :icon="item.icon"
                                 :key="item.name"
                        >
                          <DesignerDataData v-if="item.type=='data'"
                                              :directory_id="item.directory_id"
                                              :directory_name="item.name" :split_value="split"></DesignerDataData>
                          <DesignerLogicData v-if="item.type=='logic'" :directory_id="item.directory_id"
                                             :directory_name="item.name"></DesignerLogicData>

                        </TabPane>
                    </Tabs>
                </div>
            </Split>
        </span>
    </div>
  </div>
</template>

<script>
    import Directory from '../../../component/directory/Directory.vue'
    import DesignerDataData from "./DataBoardData";
    import {Tabs} from "view-design";
    import DesignerLogicData from "../../designer/designer_logic/designer_logic_data/DesignerLogicData";

    export default {
        name: "DataBoard",
        components: {
            DesignerLogicData,
            Directory,
            DesignerDataData,
            Tabs
        },
        data() {
            return {
                //
                is_databoard: true,
                // service type list
                service_type_list: ['data'],
                // menu
                menu_active_name: "data",
                // breadcrumb
                breadcrumb: {
                    list: [],
                },
                // directory
                directory: {
                    cur_id: '',
                },
                // split
                split: 0.2,
                // tab_panel
                tab_panel: {
                    if: false,
                },
                tab_pane: [],
                tab_pane_cur: -1,
                tab_panel_cur_id: "",
            }
        },
        methods: {
            beforeRemove(index) {
                const component = this;
                return new Promise(function (resolve, reject) {
                    let real_index = 0;
                    let index_increment = index;
                    component._data.tab_pane_cur = -1;
                    for (const index in component._data.tab_pane) {
                        const item = component._data.tab_pane[index];
                        if (item['visible']) {
                            if (0 == index_increment) {
                                real_index = index;
                            } else if (-1 == index_increment) {
                                component._data.tab_pane_cur = parseInt(index);
                                break;
                            }
                            index_increment--;
                            continue;
                        }
                    }
                    component._data.tab_pane[real_index].visible = false;
                    reject(index);
                })
            },
            onClickTab(index) {
                const tab_data = this._data.tab_pane[index];
                // breadcrumb
                this._data.breadcrumb.list = tab_data['breadcrumb_list'];
                this._data.directory.cur_id = tab_data['directory_id'];
                // menu
                this._data.menu_active_name = tab_data['type'];
                // tab
                this._data.tab_panel_cur_id = this._data.tab_pane[index]["name"];
            },
            handleTabRemove(index) {
            },
            OnClickDirectory(service_type, directory) {
                const _id = directory["id"];
                const name = directory["name"];
                // set breadcrumb
                const breadcrumb_list = [name];
                this._data.directory.cur_id = _id;
                let parent = directory["parent"];
                while (parent) {
                    breadcrumb_list.push(parent["name"]);
                    if (parent["parent"]) parent = parent["parent"];
                    else parent = null;
                }
                breadcrumb_list.pop();
                this._data.breadcrumb.list = breadcrumb_list.reverse();

                const cur_service_type = this._data.menu_active_name;
                let label = name;
                const tab_panel_id = cur_service_type + _id;
                this._data.tab_panel_cur_id = tab_panel_id;
                for (const index in this._data.tab_pane) {
                    const item = this._data.tab_pane[index];
                    if (item['name'] == tab_panel_id) {
                        // is_not_exist = false;
                        this._data.tab_pane_cur = parseInt(index);
                        this._data.tab_pane[index].visible = true;
                        return;
                    }
                    if (label == item['label']) {
                        label = breadcrumb_list.join(" / ");
                    }
                }
                let icon = 'md-albums';
                if (cur_service_type == 'logic') {
                    icon = 'md-cog';
                }
                this._data.tab_pane.push({
                    'type': cur_service_type,
                    'name': tab_panel_id,
                    'directory_id': _id,
                    'breadcrumb_list': breadcrumb_list,
                    'label': label,
                    'visible': true,
                    'icon': icon,
                });
                this._data.tab_pane_cur = this._data.tab_pane.length - 1;
            },
        },
    }
</script>

<style>
  @import '../../../../node_modules/view-design/dist/styles/iview.css';

  .ivu-split-trigger-vertical {
    width: 2px;
    background: #d6d6d6;
  }

  .ivu-split-trigger {
    border: 0px;
  }

  .ivu-tabs-bar {
    margin-bottom: 1px;
  }

  .ivu-menu-vertical .ivu-menu-item, .ivu-menu-vertical .ivu-menu-submenu-title {
    padding: 0 0px;
  }

  .ivu-breadcrumb {
    font-size: 22px;
    float: left;
  }

  .ivu-menu-horizontal {
    height: 30px;
    line-height: 30px;
  }
</style>

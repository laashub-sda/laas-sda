<template>
  <div>
    <Button @click="init_tree">Refresh</Button>
    <Button v-if="!is_databoard" @click="onAddNode(null)">Add</Button>
    <vue-tree-list
      @click="onClick"
      @change-name="onChangeName"
      @delete-node="onDel"
      @add-node="onAddNode"
      @drop="onDrop"
      :model="tree"
      default-tree-node-name="new"
      default-leaf-node-name="new"
      v-bind:default-expanded="true"
    >
      <span v-if="is_databoard" class="icon" slot="addTreeNodeIcon"></span>
      <span v-if="is_databoard" class="icon" slot="addLeafNodeIcon"></span>
      <span v-if="is_databoard" class="icon" slot="editNodeIcon"></span>
      <span v-if="is_databoard" class="icon" slot="delNodeIcon"></span>
      <span v-if="is_databoard" class="icon" slot="leafNodeIcon"></span>
      <span v-if="is_databoard" class="icon" slot="treeNodeIcon"></span>
    </vue-tree-list>
  </div>
</template>

<script>
    import {Tree, TreeNode, VueTreeList} from 'vue-tree-list'
    import directory from './directory.js'

    export default {
        name: "Directory",
        props: {
            "is_databoard": {
                type: Boolean,
                default: false,
                required: false,
            },
            "service_type": {
                type: String,
                default: "data",
            },
            "del-directory": Function,
            "change-directory": Function,
            "add-directory": Function,
            "drop-directory": Function,
            "click-directory": Function,
        },
        components: {
            VueTreeList
        },
        data() {
            return {
                tree: new Tree([]),
                name: "",
                newTree: {},
            }
        },
        methods: {
            async onDel(node) {
                // delete need to confirm
                const component = this;
                if (!await new Promise(function (resolve, reject) {
                    component.$Modal.warning({
                        title: "tips",
                        content: "are you ready to delete?",
                        okText: "YES",
                        onOk: function () {
                            resolve(true);
                        },
                        closable: true,
                        onCancel: function () {
                            resolve(false);
                        },
                        cancelText: "NO"
                    });
                })) return;
                // save
                try {
                    const insert_result = await directory.delete_(this.service_type, {
                        "id": node["id"],
                    });
                    this.$Message.success('delete directory success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
                node.remove();
                this.$emit('del-directory', this.service_type, node);
            },

            async onChangeName(params) {
                // if ('blur' != params["eventType"]) return;
                const input_name_result = params["newName"];
                if ("" == input_name_result) {
                    this.$Message.error("name can't be blank character");
                    return;
                }
                // save
                try {
                    const insert_result = await directory.update_(this.service_type, {
                        "id": params["id"],
                        "name": input_name_result,
                    });
                    this.$Message.success('update directory name success');
                    this.$emit('change-directory', this.service_type, params);
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }

            },

            async onAddNode(params) {
                // make sure input data directory name
                const component = this;
                component._data.name = "";
                const input_name_result = await new Promise(function (resolve, reject) {
                    component.$Modal.confirm({
                        onOk: () => {
                            resolve(component._data.name);
                        },
                        onCancel: () => {
                            component._data.name = "";
                            resolve(component._data.name);
                        },
                        render: (h) => {
                            // TODO improvement: input box can autofocus
                            return h('Input', {
                                props: {
                                    autofocus: true,
                                    placeholder: 'Please enter directory name(a-z0-9_)...',
                                },
                                on: {
                                    input: (val) => {
                                        component._data.name = val;
                                    }
                                }
                            })
                        }
                    })
                });
                if ("" == input_name_result) return;
                let pid = -1;
                // special for top level tree node
                if (params) {
                    pid = params["pid"];
                    params["addLeafNodeDisabled"] = true;
                    params["name"] = input_name_result;
                }
                // save
                try {
                    const insert_result = await directory.insert_(this.service_type, {
                        "pid": pid,
                        "name": input_name_result,
                    });
                    if (!params) {
                        params = {
                            id: insert_result,
                            name: input_name_result,
                            pid: pid,
                            isLeaf: false,
                            addLeafNodeDisabled: true,
                            children: []
                        };
                        this._data.tree.addChildren(new TreeNode(params));
                    } else {
                        params["id"] = insert_result;
                    }
                    this.$Message.success('insert directory success');
                    this.$emit('add-directory', this.service_type, params);
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
            },
            async onDrop(params) {
                // save
                try {
                    const insert_result = await directory.update_(this.service_type, {
                        "id": params["node"]["id"],
                        "pid": params["target"]["id"],
                    });
                    this.$Message.success('update directory name success');
                    this.$emit('drop-directory', this.service_type, params);
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
            },
            onClick(params) {
                this.$emit('click-directory', this.service_type, params);
            },
            async init_tree() {
                try {
                    this._data.tree = new Tree(await directory.select_tree(this.service_type));
                    this.$Message.success('select directory success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
            },
        },
        async created() {
            await this.init_tree();
        },
    }
    // TODO improvement: support version and fork operation for every data
</script>


<style lang="less" rel="stylesheet/less" scoped>
  .vtl {
    .vtl-drag-disabled {
      background-color: #d0cfcf;

      &:hover {
        background-color: #d0cfcf;
      }
    }

    .vtl-disabled {
      background-color: #d0cfcf;
    }
  }
</style>

<style lang="less" rel="stylesheet/less" scoped>
  .icon {
    &:hover {
      cursor: pointer;
    }
  }
</style>
<style>
  .vtl-node-main .vtl-operation {
    letter-spacing: 10px;
  }

  @import '~view-design/dist/styles/iview.css';
</style>

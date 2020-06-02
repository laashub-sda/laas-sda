<template>
  <div style="height: 93vh;border: 1px solid #d6d6d6;">
        <span style="height:93vh;">
            <Split v-model="split">
                <div slot="left">
                  <Directory @click-directory="OnClickDirectory" service_type="logic"></Directory>
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
                          <DesignerLogicData :directory_id="item.directory_id"
                                             :directory_name="item.name"></DesignerLogicData>

                        </TabPane>
                    </Tabs>
                </div>
            </Split>
        </span>
  </div>
</template>
<script>
    export default {
        name: "DesignerLogicData",
        components: {},
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
                default: 0.1,
            },
        },
        data() {
            return {
                split: 0.2,
                tab_pane: [],
                tab_pane_cur: '',
            }
        },
        methods: {
            OnClickDirectory: function () {

            },
            handleTabRemove: function () {

            },
            onClickTab: function () {

            },
            beforeRemove: function () {

            },
        },
        async created() {
        },
    }
</script>

<style>
</style>

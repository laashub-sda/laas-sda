<template>
  <div>
    <Row>
      <Col span="23">
        <i-input v-model="description"
                 :readonly="description_disabled"
                 type="textarea">
        </i-input>
      </Col>
      <Col span="1">
        <Button @click="update_directory_description" style="height: 100%">
          <span style="writing-mode:vertical-rl">{{description_btn_name}}</span>
        </Button>
      </Col>
    </Row>
  </div>
</template>

<script>
    import directory from "./directory";

    const update_description_btn_str = "UPDATE";
    const save_description_btn_str = "SAVE";

    export default {
        name: "DirectoryDescription",
        props: {
            "directory_id": {
                required: false,
            }
        },
        data() {
            return {
                description: "",
                description_disabled: true,
                description_btn_name: update_description_btn_str,
            }
        },
        methods: {
            async init_description() {
                const data_directory = {
                    'id': this.directory_id,
                }
                try {
                    const data_directory_result = await directory.select_("data", data_directory);
                    this._data.description = data_directory_result[0].description;
                    this.$Message.success('select data directory description success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }

            },
            async update_directory_description() {
                if (this._data.description_disabled) {
                    this._data.description_disabled = false;
                    this._data.description_btn_name = save_description_btn_str;
                    return;
                }
                this._data.description_disabled = true;
                this._data.description_btn_name = update_description_btn_str;
                const data_directory = {
                    'id': this.directory_id,
                    'description': this._data.description,
                }
                try {
                    await directory.update_("data", data_directory);
                    this.$Message.success('update data directory description success');
                } catch (e) {
                    console.log(e);
                    this.$Message.error(e.response.data);
                }
            },
        },
        async created() {
            await this.init_description();
        }
    }
</script>

<style scoped>

</style>

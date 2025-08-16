<template>
    <form v-if="defaults" v-on:submit.prevent="updateM2MForm($event)">
        <RowForm v-bind:row="defaults" v-bind:schema="M2MSchema" />
        <button>{{ $t("Update") }}</button>
    </form>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import RowForm from "../components/RowForm.vue"
import { convertFormValue } from "../utils"
import type { APIResponseMessage } from "../interfaces"

export default defineComponent({
    props: {
        tableName: String,
        selectedRows: {
            type: Array,
            default: () => []
        }
    },
    components: {
        RowForm
    },
    data() {
        return {
            defaults: {} as { [key: string]: any },
            buttonEnabled: true
        }
    },
    computed: {
        M2MSchema() {
            return this.$store.state?.schema
        }
    },
    methods: {
        async updateM2MForm(event: Event) {
            console.log("Updating M2M rows ...")

            // We prevent the button from being clicked again until we've
            // finished, as it can cause many API requests.
            this.buttonEnabled = false

            const form = new FormData(event.target as HTMLFormElement)

            const json: { [key: string]: any } = {}
            for (const i of form.entries()) {
                const key = i[0]
                let value = i[1]
                json[key] = convertFormValue({
                    key,
                    value,
                    schema: this.M2MSchema
                })
            }

            try {
                // TODO - we will use the new bulk update endpoint once it is
                // merged into PiccoloCRUD.
                for (let i = 0; i < this.selectedRows.length; i++) {
                    await this.$store.dispatch("updateRow", {
                        tableName: this.tableName,
                        rowID: this.selectedRows[i],
                        data: json
                    })
                }
                var message: APIResponseMessage = {
                    contents: "Successfully updated rows",
                    type: "success"
                }
                this.$store.commit("updateApiResponseMessage", message)

                this.$emit("close")

                await this.$store.dispatch("fetchRows")
            } catch (error) {
                console.log(error)
                var message: APIResponseMessage = {
                    contents: "Invalid column name or value",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            this.buttonEnabled = true
        }
    }
})
</script>
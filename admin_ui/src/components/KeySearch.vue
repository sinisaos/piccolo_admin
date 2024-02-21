<template>
    <div class="key_search">
        <input
            autocomplete="off"
            :placeholder="isFilter ? 'All' : 'None'"
            type="text"
            v-model="selectedValue"
            v-on:focus="showModal = true"
            v-on:keydown.enter.prevent
        />

        <input
            :value="hiddenSelectedValue"
            type="hidden"
            v-bind:name="fieldName"
        />

        <KeySearchModal
            v-if="tableName"
            v-show="showModal"
            :isFilter="isFilter"
            :tableName="tableName"
            @close="showModal = false"
            @update="handleUpdate($event)"
        />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import KeySearchModal from "./KeySearchModal.vue"
import type { RowID } from "@/interfaces"

export default defineComponent({
    props: {
        fieldName: {
            type: String as PropType<string>,
            required: true
        },
        tableName: {
            type: String as PropType<string>,
            required: true
        },
        rowID: {
            type: undefined as unknown as PropType<RowID | undefined>
        },
        readable: {
            type: String as PropType<string>
        },
        isFilter: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        isNullable: {
            type: Boolean as PropType<boolean>,
            default: false
        }
    },
    data() {
        return {
            ids: [],
            selectedValue: undefined as string | undefined,
            hiddenSelectedValue: undefined as RowID | undefined,
            showModal: false
        }
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        isTargetColumn() {
            for (const key in this.schema.properties) {
                if (key == this.tableName) {
                    return Object.values(
                        this.schema.extra.target_column
                    ).includes(
                        this.schema.properties[key].extra.foreign_key
                            ?.target_column
                    )
                }
            }
        }
    },
    methods: {
        handleUpdate(event: any) {
            this.selectedValue = event.readable
            this.hiddenSelectedValue =
                this.isTargetColumn == false || this.isFilter == true
                    ? event.id
                    : event.readable
            this.showModal = false
            this.$emit("update", event)
        }
    },
    components: {
        KeySearchModal
    },
    watch: {
        readable(newValue) {
            this.selectedValue = newValue
        },
        rowID(newValue) {
            this.hiddenSelectedValue = newValue
        }
    },
    async mounted() {
        this.selectedValue = this.readable
        this.hiddenSelectedValue = this.rowID
    }
})
</script>

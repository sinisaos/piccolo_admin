<template>
    <div id="overlay">
        <div class="modal opaque">
            <p class="close">
                <a
                    class="subtle"
                    href="#"
                    v-on:click.prevent="$emit('close')"
                >
                    <font-awesome-icon icon="times" />
                </a>
            </p>

            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {}
</script>

<style scoped lang="less">
div#overlay {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.7);
    overflow: auto;

    div.modal {
        border-radius: 0.5rem;
        box-sizing: border-box;
        margin: 1rem auto;
        max-width: 100%;
        padding: 1rem;
        width: 30rem;

        label,
        input {
            width: 100%;
            display: block;
        }

        p.close {
            text-align: right;
        }
    }
}
</style>

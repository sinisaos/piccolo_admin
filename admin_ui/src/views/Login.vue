<template>
    <div id="login">
        <div class="logo">
            <a href="https://github.com/piccolo-orm/piccolo_admin">
                <img src="https://raw.githubusercontent.com/piccolo-orm/piccolo_admin/master/docs/logo_hero.png" alt="">
            </a>
        </div>
        <div class="inner">
            <div class="heading">
                <h1>{{ siteName }}</h1>
            </div>
            <form v-on:submit.prevent="login">
                <label>{{ $t("Username") }}</label>
                <input name="username" type="text" v-model="username" placeholder="Enter username" />

                <label>{{ $t("Password") }}</label>
                <PasswordInput @input="password = $event" :value="password" />

                <template v-if="mfaCodeRequired">
                    <label>{{ $t("MFA Code") }}</label>
                    <input placeholder="123456" type="text" v-model="mfaCode" />
                    <p>
                        Hint: Use your authenticator app to generate the MFA
                        code - if you've lost your phone, you can use a recovery
                        code instead.
                    </p>
                </template>

                <button data-uitest="login_button">{{ $t("Login") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import axios from "axios"
import PasswordInput from "../components/PasswordInput.vue"

export default defineComponent({
    data() {
        return {
            username: "",
            password: "",
            mfaCode: "",
            mfaCodeRequired: false
        }
    },
    components: {
        PasswordInput
    },
    computed: {
        siteName(): string {
            return this.$store.state.metaModule.siteName
        }
    },
    methods: {
        async login() {
            console.log("Logging in")
            try {
                await axios.post(`./public/login/`, {
                    username: this.username,
                    password: this.password,
                    ...(this.mfaCodeRequired ? { mfa_code: this.mfaCode } : {})
                })
            } catch (error) {
                console.log("Request failed")

                if (axios.isAxiosError(error)) {
                    console.log(error.response)

                    if (
                        error.response?.status == 401 &&
                        error.response?.data?.detail == "MFA code required"
                    ) {
                        this.$store.commit("updateApiResponseMessage", {
                            contents: "MFA code required",
                            type: "neutral"
                        })

                        this.mfaCodeRequired = true
                    } else {
                        this.$store.commit("updateApiResponseMessage", {
                            contents: "Problem logging in",
                            type: "error"
                        })
                    }
                }

                return
            }

            await this.$store.dispatch("fetchUser")

            const nextURL = this.$route.query.nextURL as string

            if (nextURL && !nextURL.startsWith("/login")) {
                await this.$router.push({ path: nextURL })
            } else {
                await this.$router.push({ name: "home" })
            }
        }
    }
})
</script>

<style lang="less">
.logo {
    display: flex; 
    justify-content: center; 
    padding-top: 2rem;
    margin-bottom: -2rem;
}

img { 
    width: 25rem;
    border-radius: .7rem;
}

div#login {
    div.inner {
        margin: auto;
        margin-top: 3rem;
        max-width: 25rem;
        box-sizing: border-box;
        padding: 1.8rem;
        border: .1rem solid #e2e8f0;
        border-radius: .7rem;
        box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.5);

        div.heading {
            text-align: center;

            h1 {
                margin-top: 0;
                padding-top: 0.8rem;
                text-align: center;
                border-bottom: 3px solid #3889ce;
                display: inline-block;
            }
        }
    }
}
</style>

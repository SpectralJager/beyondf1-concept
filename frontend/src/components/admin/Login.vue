<template>
<div class="article-modal-form login-form">
    <form class="form">
        <div class="form--header">
            <h2 class="form--title">Login</h2>
        </div>
        <div class="form--content">
            <div class="form--group">
                <label for="username">Username</label>
                <input type="text" v-model="admin.username">
            </div>
            <div class="form--group">
                <label for="password">Password</label>
                <input type="password" v-model="admin.password">
            </div>
        </div>
        <div class="form--footer">
            <button class='btn' @click.prevent="submiteForm">Submite</button>
        </div>
    </form>
</div>
</template>

<script>
export default {
    data() {
        return {
            admin: {
                username: '',
                password: '',
            },
        }
    },
    methods: {
        async submiteForm(){
            const url = window.url + '/login';
            console.log(url);
            await fetch(url, {
                method: 'POST',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                dataType: 'json',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.admin)
            })
            .then(response => response.json())
            .then((data) => {
                this.admin.username = '';
                this.admin.password = '';
                if data.code == "success"{
                    this.$parent.jwt = data.token;
                }
            });
        }
    }

}
</script>

<style>

</style>
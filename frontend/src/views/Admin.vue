<template>
<Header :is_logged="is_logged"/>
<main class="admin">
    <seciton v-if="is_logged">
        <News v-if="fl_news" :news="news" />
    </seciton>
    <section v-else>
        <Login />
    </section>
</main>
</template>

<script>
import News from '@/components/admin/News.vue';
import Header from '@/components/admin/Header.vue';
import Login from '@/components/admin/Login.vue';

export default {
    data() {
        return{
            fl_news: false,
            is_logged: false,
            news: [],
            jwt: '',
        }
    },
    methods: {
        showNews(){
            this.fetchNews();
        },
        async fetchNews(){
            const url = window.url + '/articles';
            await fetch(url, {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                dataType: 'json',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => this.news = data.articles);
            this.fl_news = true;
        }
    },
    watch: {
        jwt(newJwt, oldJwt) {
            if(newJwt != ''){
                this.is_logged = true;
            }
            else{
                this.is_logged = false;
            }
        }
    },
    components: {
        News,
        Header,
        Login
    }

}
</script>
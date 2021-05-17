<template>
<Header :is_logged="is_logged"/>
<main class="admin">
    <seciton v-if="is_logged">
        <News v-if="fl_news" :news="news" />
        <CreateNewAdmin v-elif="fl_newAdmin"/>
        <Statistic v-elif="fl_statistic" />
        <
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
        }
    },
    methods: {
        showNews(){
            this.fetchNews();
        },
        async fetchNews(){
            const url = 'http://127.0.0.1:5000/api_v1/news';
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
    components: {
        News,
        Header,
        Login
    }

}
</script>
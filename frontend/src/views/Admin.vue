<template>
<header class="header--admin">
    <div class="logo"><span>Admin Panel</span></div>
    <nav class="navbar">
        <span class="navbar--link" @click="showNews">
            News
        </span>
    </nav>
    <News v-if="fl_news" :news="news" />
</header>
</template>

<script>
import News from '@/components/admin/News.vue';
export default {
    data() {
        return{
            fl_news: false,
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
    }

}
</script>

<style>

</style>
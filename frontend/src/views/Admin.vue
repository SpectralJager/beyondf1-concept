<template>
<Header />
<main class="admin">
<News v-if="fl_news" :news="news" />
</main>
</template>

<script>
import News from '@/components/admin/News.vue';
import Header from '@/components/admin/Header.vue';
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
            const url = 'http://192.168.0.106:5000/api_v1/news';
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
    }

}
</script>
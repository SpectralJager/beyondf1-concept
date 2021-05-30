<template>
<Header />
<main class="home" v-if="showArticles">
    <ArticleItem v-for="article in articles" :key="article.id" :article="article"/>
</main>
</template>

<script>
import Header from '@/components/home/Header.vue';
import ArticleItem from '@/components/home/ArticleItem.vue';

export default {
    components: {
        Header,
        ArticleItem,
    },
    data(){
        return{
            articles: [],
            showArticles: true,
        }
    },
    methods: {
        async fetchNews(){
            const url = 'http://127.0.0.1:8000/api/v1/article/';
            await fetch(url, {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                dataType: 'json',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => this.articles = data);
        }
    },
    mounted() {
        this.fetchNews();
    }
}
</script>


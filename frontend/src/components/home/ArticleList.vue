<template>
<main class="home" v-if="showArticle">
    <ArticleListItem v-for="article in articles" :key="article.id" :article="article"/>
</main>
</template>

<script>
import ArticleListItem from '@/components/home/ArticleListItem.vue';

export default {
    components: {
        ArticleListItem,
    },
    data() {
        return {
            articles: {},
            showArticle: true,
        }
    },
    methods: {
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
            .then(data => this.articles = data.articles);
        }
    },
    mounted() {
        this.fetchNews();
    }
}
</script>

<style>

</style>
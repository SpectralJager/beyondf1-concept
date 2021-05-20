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
            const url = window.url + '/news';
            await fetch(url, {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                dataType: 'json',
                headers: {
                    'Content-Type': 'application/json',
                    'Origin': 'http://127.0.0.1'
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
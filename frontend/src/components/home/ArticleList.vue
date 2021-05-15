<template>
<main class="home" v-show="showArticles">
    <ArticleListItem />
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
            showArticle: false,
        }
    },
    methods: {
        fetchArticles() {
            console.log('fetching articles from api')
            return {}
        }
    },
}
</script>

<style>

</style>
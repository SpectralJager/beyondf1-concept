<template>
<Header />
<main class="article-read">
    <section class="read">
        <h1 class="title">{{ article.title }}</h1>
        <p class="meta">{{ article.published_date }}</p>
        <p class="text" v-html="article.text"></p>
        <a :href="article.source" class="source">{{ article.domain }}</a>
    </section>
    <section class="articles">
        some articles
    </section>
</main>
</template>

<script>
import Header from '@/components/home/Header.vue';

export default {
    props: {
        id: String,
    },
    components: {
        Header,
    },
    data() {
        return {
            article: {},
        }
    },
    methods: {
        async fetchNews(){
            const url = 'http://127.0.0.1:5000/api_v1/news/' + this.id;
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
            .then(data => this.article = data.article);
        }
    },
    mounted() {
        this.fetchNews();
    }



}
</script>

<style>

</style>
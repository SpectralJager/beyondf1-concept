<template>
<div class="article">
    <div class="img" :style="'--bg-img: url('+ article.bg_url + ');'"></div>
    <div class="content">
        <h2 class="title">{{ article.title }}</h2>
        <p class="meta">{{ Date(article.date) }}</p>
        <div class="text" v-html="prev_text">
        </div>
        <div class="btn-wrapper"><router-link :to="'/articles/' + article.id">Read more</router-link></div>
    </div>
</div> 
</template>

<script>
export default {
    props: {
        article: Object,
    },
    data(){
        return {
            prev_text: this.article.content.slice(0,100) + '...',
        }
    }
}
</script>
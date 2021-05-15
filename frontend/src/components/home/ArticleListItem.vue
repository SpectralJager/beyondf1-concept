<template>
<div class="article">
    <div class="img" :style="'--bg-img: url('+ article.bg_url + ');'"></div>
    <div class="content">
        <h2 class="title">{{ article.title }}</h2>
        <p class="meta">{{ article.date }}</p>
        <div class="text">
            
        </div>
        <a :href="'/articles/' + article.id" class="btn">Read more</a>
    </div>
</div> 
</template>

<script>
export default {
    props: {
        article: Object,
    }
}
</script>

<style>

</style>
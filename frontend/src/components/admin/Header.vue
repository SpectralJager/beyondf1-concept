<template>
<header class='header--home' :style="'--bg-img: url('+ bg_url +');'">
    <h1 class="title">Beyond<span class='font-red'>F1</span> - Admin</h1>
    <nav class='navigation'>
        <router-link to="/">Site</router-link>
        <a @click="$parent.showNews">News</a>
    </nav>
    <div class="bottom-content">
        <div class="links">
            <i class="fab fa-linkedin"></i>
            <i class="fab fa-github-square"></i>
            <i class="fab fa-codepen"></i>
        </div>
    </div>
</header>
</template>

<script>
export default {
    data() {
        return{
            bg_url: require("@/assets/img/header-bg.jpg"),
        }
    }

}
</script>
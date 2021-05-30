<template>
<header class='header--home' :style="'--bg-img: url('+ bg_url +');'">
    <h1 class="title">Beyond<span class='font-red'>F1</span></h1>
    <nav class='navigation'>
        <router-link to="/">Home</router-link>
        <a to="/wiki" class='disabled-link'>Wiki</a>
        <a to="/contacts" class='disabled-link'>Contacts</a>
    </nav>
    <div class="bottom-content">
        <span class="sub-text">Subscribe for updates</span>
        <form method="post">
            <input type="email" name="email" id="email" placeholder="Enter your email">
            <button type="submit"><i class="fas fa-paper-plane"></i></button>
        </form>
        <div class="links">
            <i class="fab fa-linkedin"></i>
            <i class="fab fa-github-square"></i>
            <i class="fab fa-twitter-square"></i>
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

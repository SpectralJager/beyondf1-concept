<template>
<div class="container">
    <h1 calss="section--title">News</h1>
    <hr>
    <button class="btn" @click="createArticle">Create new Article</button>
    <div class="section--content">
        <table>
            <thead>
                <th>#</th>
                <th>Title</th>
                <th>Site</th>
                <th>Publicated date</th>
                <th></th>
            </thead>
            <tbody>
                <tr v-for="article in news" :key="article.id">
                    <td>{{article.id}}</td>
                    <td>{{article.title}}</td>
                    <td>{{article.domain}}</td>
                    <td>{{article.published_date}}</td>
                    <td>
                        <button class="btn" @click="editArticle(article)">Edit</button>
                        <button class="btn" @click="deleteArticle(article.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
<AddArticle v-if="fl_form" :is_editing="is_editing" :article="edit_article" /> 
</template>

<script>
import AddArticle from '@/components/admin/AddArticle.vue';

export default {
    components:{
        AddArticle
    },
    props: {
        news: Object,
    },
    data() {
        return{
            fl_form: false,
            is_editing: false,
            edit_article: {
                title: '',
                domain: '',
                source: '',
                bg_url: '',
                text: '',
            },
            
        }
    },
    methods: {
        createArticle(){
            this.fl_form = true;   
        },
        editArticle(article){
            this.edit_article = article;
            this.is_editing = true;
            this.fl_form = true;
        },
        async deleteArticle(id){
            const url = 'http://127.0.0.1:5000/api_v1/news/' + id;
            console.log(url);
            await fetch(url, {
                method: 'DELETE',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                dataType: 'json',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
            this.$parent.fetchNews();
        },
        
    }

}
</script>
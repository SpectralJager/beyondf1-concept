<template>
<div class="container">
    <h1>News</h1>
    <hr>
    <button class="btn" @click="fl_form = true">Create new Article</button>
    <form v-if="fl_form" class="form">
        <div class="form--group">
            <label for="title">Title</label>
            <input type="text" v-model="title">
        </div>
        <div class="form--group">
            <label for="domain">Domain</label>
            <input type="text" v-model="domain">
        </div>
        <div class="form--group">
            <label for="source">Source</label>
            <input type="text" v-model="source">
        </div>
        <div class="form--group">
            <label for="bg_url">Background image url</label>
            <input type="text" v-model="bg_url">
        </div>
        <div class="form--group">
            <label for="text"></label>
            <ckeditor :editor="editor" v-model="text" :config="editorConfig"></ckeditor>
        </div>
        <div class="form--group">
            <button class='btn' @click="fl_form = false">Close</button>
            <button class='btn' @click.prevent="sendForm">Save</button>
        </div>
    </form>
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
                    <button class="btn">Edit</button>
                    <button class="btn" @click="deleteArticle(article.id)">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>  
</template>

<script>
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

export default {
    props: {
        news: Object,
    },
    data() {
        return{
            fl_form: false,
            title: '',
            domain: '',
            source: '',
            bg_url: '',
            text: '',
            editor: ClassicEditor,
            editorConfig: {
                // The configuration of the editor.
            }
        }
    },
    methods: {
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
        async sendForm(){
            const article = {
                title: this.title,
                domain: this.domain,
                source: this.source,
                bg_url: this.bg_url,
                text: this.text,
            };
            console.log(article);
            const url = 'http://127.0.0.1:5000/api_v1/news';
            console.log(url);
            await fetch(url, {
                method: 'POST',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                dataType: 'json',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(article)
            });
            this.$parent.fetchNews();
        }
    }

}
</script>

<style>

</style>
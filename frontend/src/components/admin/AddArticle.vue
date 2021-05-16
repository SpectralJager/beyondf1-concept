<template>
<div class="article-modal-form">
    <form class=" form">
        <div class="form--header">
            <h2 class="form--title" v-if="is_editing">Edit Article: #{{article.id}}</h2>
            <h2 class="form--title" v-else>Create Article</h2>
        </div>
        <div class="form--content">
            <div class="form--group">
                <label for="title">Title</label>
                <input type="text" v-model="article.title">
            </div>
            <div class="form--group">
                <label for="domain">Domain</label>
                <input type="text" v-model="article.domain">
            </div>
            <div class="form--group">
                <label for="source">Source</label>
                <input type="text" v-model="article.source">
            </div>
            <div class="form--group">
                <label for="bg_url">Background image url</label>
                <input type="text" v-model="article.bg_url">
            </div>
            <div class="form--group">
                <!--<label for="text">Text</label>-->
                <ckeditor :editor="editor" v-model="article.text" tag-name="textarea"></ckeditor>
            </div>
        </div>
        <div class="form--footer">
            <button class='btn' @click.prevent="hideForm">Close</button>
            <button class='btn' @click.prevent="saveForm">Save</button>
        </div>
    </form>
</div>
</template>

<script>
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

export default {
    props: {
        is_editing: Boolean,
        article: Object,
    },
    data(){
        return{
            
            // CKEditor
            editor: ClassicEditor,
        }
    },
    methods: {
        hideForm(){
            this.$parent.edit_article = {
                title: '',
                domain: '',
                source: '',
                bg_url: '',
                text: '',
            };
            this.$parent.fl_form = false;
            this.$parent.is_editing = false;
        },
        async saveForm(){
            console.log(this.article);
            let url = 'http://192.168.0.106:5000/api_v1/news';
            if(this.is_editing){
                url = url + "/" + this.article.id;
                console.log(url);
                await fetch(url, {
                    method: 'PUT',
                    mode: 'cors',
                    cache: 'no-cache',
                    credentials: 'same-origin',
                    dataType: 'json',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.article)
                }).then(response => response.json())
                .then(data => console.log(data.message));
            }
            else{
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
                    body: JSON.stringify(this.article)
                }).then(response => response.json())
                .then(data => console.log(data.message));
            }
            this.$parent.edit_article = {
                title: '',
                domain: '',
                source: '',
                bg_url: '',
                text: '',
            };
            this.$parent.fl_form = false;
            this.$parent.is_editing = false;
            this.$parent.$parent.fetchNews();
        }
    },
}
</script>

<style>

</style>
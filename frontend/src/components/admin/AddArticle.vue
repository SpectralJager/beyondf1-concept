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
                <label for="image_url">Background image url</label>
                <input type="text" v-model="article.image_url">
            </div>
            <div class="form--group">
                <!--<label for="text">Text</label>-->
                <ckeditor :editor="editor" v-model="article.content" tag-name="textarea"></ckeditor>
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
                image_url: '',
                content: '',
            };
            this.$parent.fl_form = false;
            this.$parent.is_editing = false;
        },
        async saveForm(){
            let url = window.url + '/news';
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
                image_url: '',
                content: '',
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
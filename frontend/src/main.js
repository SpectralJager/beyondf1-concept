import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import CKEditor from '@ckeditor/ckeditor5-vue';

createApp(App).use(router).use( CKEditor ).mount('#app')

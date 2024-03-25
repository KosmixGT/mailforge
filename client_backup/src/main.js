import { createApp } from "vue";
import App from "./App.vue";
import router from "./router.js";
import "./axios";
import '@mdi/font/css/materialdesignicons.css'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives
})

import TheHeader from "../src/components/layout/TheHeader.vue";
import TheFooter from "../src/components/layout/TheFooter.vue";
import { useAuthStore } from './components/store/userAuth.js';
import { useMailingStore } from './components/store/mailingStore.js';
import { createPinia } from "pinia";

const app = createApp(App);

const pinia = createPinia();

app.component("the-header", TheHeader);
app.component("the-footer", TheFooter);

app.use(vuetify);
app.use(router);
app.use(pinia);

// Инициализация состояния аутентификации при запуске приложения
useAuthStore().initialize();
useMailingStore().onInit();

app.mount("#app");
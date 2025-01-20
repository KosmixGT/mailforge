import { createApp } from "vue";
import App from "./App.vue";
import router from "./router.js";
import "./axios";
import '@mdi/font/css/materialdesignicons.css'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

const customDarkTheme = {
  dark: true,
  colors: {
    background: "#15202b",
    surface: "#15202b",
    primary: "#3f51b5",
    secondary: "#03dac6",
    error: "#f44336",
    info: "#2196F3",
    success: "#4caf50",
    warning: "#fb8c00",
  },
};
const customLightTheme = {
  dark: false,
  colors: {
    background: "#eee",
    surface: "#15202b",
    primary: "#3f51b5",
    secondary: "#00ccff",
    error: "#ffcc00",
  },
};

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "customDarkTheme",
    themes: {
      customDarkTheme,
      customLightTheme
    },
  },
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
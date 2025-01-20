<template>
  <v-app-bar app color="primary" :fixed="true">
    <v-toolbar-title class="white--text">
      <router-link to="/" class="app-name">MailForge</router-link>
    </v-toolbar-title>
    <v-btn text to="/dashboard">Панель инструментов</v-btn>
    <v-btn text to="/mailings">Рассылки</v-btn>
    <!-- <v-btn text to="/templates">Шаблоны</v-btn> -->
    <v-btn text to="/historyMailings">История</v-btn>
    <!-- Другие вкладки -->
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-switch inset color="info" @change="toggleTheme()" prepend-icon="mdi-theme-light-dark" class="mr-16 d-flex align-center justify-center"></v-switch>
      <v-btn v-if="!isLoggedIn" @click="goToRegistration">Регистрация</v-btn>
      <v-btn v-if="!isLoggedIn" @click="goToLogin">Вход</v-btn>
      <v-btn v-if="isLoggedIn" @click="logout">Выйти - {{ authStore.user.user_data.username }}</v-btn>
    </v-toolbar-items>
  </v-app-bar>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/userAuth.js";

import { useTheme } from 'vuetify'

export default {
  data() {
    return {
    };
  },
  created() {
    // Initialization code here if needed
  },
  methods: {
    goToRegistration() {
      this.$router.push({ name: 'Registration' });
    },
    goToLogin() {
      this.$router.push({ name: 'Authorization' });
    },
    async logout() {
      this.authStore.logout();
    }

  },
  setup() {
    const theme = useTheme();
    const router = useRouter();
    const authStore = useAuthStore();
    const isLoggedIn = computed(() => authStore.$state.isAuthenticated);
    const toggleTheme = () => {
      if (theme.global.current.value.dark) {
        theme.global.name.value = 'light';
      } else {
        theme.global.name.value = 'customDarkTheme';
      }
    };

    return { router, authStore, isLoggedIn, toggleTheme };
  }
}
</script>


<style scoped>
.app-name {
  position: relative;
  font-size: 24px;
  letter-spacing: 1px;
  color: rgb(255, 255, 255);
  transition: color 0.3s;
  /* Плавное изменение цвета */
}

.app-name:hover {
  color: rgb(38, 219, 32);
}

.app-name:hover::before {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border: 50px solid rgba(255, 255, 255, 0.116);
  border-radius: 10px;
  z-index: -1;
}


.v-btn {
  color: white !important;
  /* Цвет текста кнопки */
}

@media only screen and (max-width: 768px) {
  .app-name {
    font-size: 20px;
  }
}
</style>

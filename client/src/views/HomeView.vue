<template>
  <v-container>
    <v-row v-if="authStore.isAuthenticated">
      <v-col>
        <h1>Вы вошли в систему</h1>
        <ProfileView />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col>
        <h1>Добро пожаловать в приложение MailForge!</h1>
        <h2>Мощный инструмент для управления рассылками и коммуникацией с вашей аудиторией</h2>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { defineAsyncComponent } from "vue";
import { useAuthStore } from "../components/store/userAuth";

const ProfileView = defineAsyncComponent(() => import("./ProfileView.vue"));

const authStore = useAuthStore();
</script>

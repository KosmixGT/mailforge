<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="headline grey lighten-2">
            Авторизация
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submitLogDetails">
              <v-text-field v-model="username" label="Имя пользователя или почта" required @blur="clearError"></v-text-field>
              <v-row>
                <v-col cols="10">
                  <v-text-field v-model="password" label="Пароль" :type="passwordType" required
                    @blur="clearError"></v-text-field>
                </v-col>
                <v-col cols="2" class="d-flex align-center">
                  <v-btn icon @click="togglePasswordVisibility"
                    :class="{ 'show-password': passwordType === 'password' }">
                    <v-icon>
                      {{ passwordType === 'password' ? 'mdi-eye' : 'mdi-eye-off' }}
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-btn color="primary" type="submit" block>Войти</v-btn>
            </v-form>
            <v-alert v-if="errorLogIn" type="error" dismissible>
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../components/store/userAuth.js";

const authStore = useAuthStore();
const username = ref("");
const password = ref("");
const passwordType = ref("password");

const { errorMessage, errorLogIn } = authStore;

async function submitLogDetails() {
  await authStore.login(username.value, password.value);
}

function togglePasswordVisibility() {
  passwordType.value = passwordType.value === "password" ? "text" : "password";
}

function clearError() {
  authStore.clearError();
}
</script>

<style scoped>
.show-password {
  color: #757575;
}
</style>

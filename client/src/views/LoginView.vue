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
              <v-btn :disabled="isLoading" color="primary" type="submit" block>
                <span v-if="isLoading">
                  <v-icon left>mdi-loading</v-icon> Загрузка...
                </span>
                <span v-else>Войти</span>
              </v-btn>
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

<script>
import { useAuthStore } from "../components/store/userAuth.js";

export default {
  data() {
    return {
      username: '',
      password: '',
      passwordType: 'password',
      authStore: useAuthStore(),
      isLoading: false
    };
  },
  computed: {
    errorMessage() {
      return this.authStore.errorMessage;
    },
    errorLogIn() {
      return this.authStore.errorLogIn;
    }
  },
  methods: {
    async submitLogDetails() {
      this.isLoading = true;
      await this.authStore.login(this.username, this.password);
      this.isLoading = false;
    },
    togglePasswordVisibility() {
      this.passwordType = this.passwordType === 'password' ? 'text' : 'password';
    },
    clearError() {
      this.authStore.clearError();
    }
  },
  created() {
    // Вы можете добавить код инициализации, если необходимо
  }
}
</script>

<style scoped>
.show-password {
  color: #757575;
}
</style>

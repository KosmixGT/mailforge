<template>
  <v-container>
    <v-card class="profile">
      <v-card-title>
        <h1 class="headline">Профиль</h1>
      </v-card-title>
      <v-card-text>
        <div>
          <p class="info-text"><strong>Имя пользователя:</strong> {{ user.user_data.username }}</p>
          <p class="info-text"><strong>Email:</strong> {{ user.user_data.email }}</p>
          <p class="info-text"><strong>Роль:</strong> {{ userRole }}</p>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '../components/store/userAuth'; // Импортируем хранилище аутентификации
import { computed } from "vue";

const authStore = useAuthStore(); // Используем хранилище аутентификации

const user = authStore.user; // Получаем данные о пользователе из хранилища

// Определяем вычисляемое свойство для определения роли пользователя
const userRole = computed(() => {
  return user.user_data.userrole === 2 ? 'Администратор' : 'Обычный пользователь';
});

</script>

<style scoped>
.profile {
  max-width: 400px;
  margin: auto;
}

.headline{
  font-size: 26px;
}
.info-text{
  font-size: 18px;
  text-align: left;
  margin: 10px;
  padding: 1px;
}
</style>

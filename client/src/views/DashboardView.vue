<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="display-1 text-center mb-6">Основные функции системы</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-card class="dashboard-card" @click="goToMailings">
          <v-card-title class="headline">Управление рассылками</v-card-title>
          <v-card-text>
            Здесь вы можете создавать, просматривать и управлять вашими рассылками. Вы можете добавить новые рассылки, изменить существующие или удалить неактуальные.
          </v-card-text>
          <v-card-actions>
            <v-btn text color="primary" @click="goToMailings">Подробнее</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="dashboard-card" @click="goToScheduledMailings">
          <v-card-title class="headline">История рассылок</v-card-title>
          <v-card-text>
            Здесь вы можете просматривать и управлять осуществлёнными рассылками. Вы можете редактировать и повторять рассылки.
          </v-card-text>
          <v-card-actions>
            <v-btn text color="primary" @click="goToScheduledMailings">Подробнее</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  methods: {
    goToMailings() {
      // Переход к управлению рассылками
      this.$router.push('/mailings');
    },
    goToScheduledMailings() {
      // Переход к запланированным рассылкам
      this.$router.push('/historyMailings');
    }
  }
}
</script>

<style scoped>
.dashboard-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  margin-bottom: 20px;
  border: 2px solid #3f51b5; /* Цвет рамки */
  border-radius: 10px; /* Закругление углов */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Тень */
}

.dashboard-card:hover {
  transform: scale(1.05);
}
</style>

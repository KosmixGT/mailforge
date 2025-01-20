<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-12">
          <v-card-text class="text-center">
            <v-icon color="error" size="64">mdi-alert-circle-outline</v-icon>
            <h1 class="headline">Страница не найдена!</h1>
            <p class="mt-4">Извините, страница, которую вы ищете, не найдена.</p>
            <p class="mt-4">Пожалуйста, попробуйте еще раз или перейдите на другую страницу.</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" to="/" class="font-weight-bold">Перейти на главную</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.mt-4 {
  margin-top: 1rem;
  font-size: 1.25rem;
  line-height: 1.5;
}

.headline {
  margin-top: 1rem;
  margin-bottom: 1rem;
  font-size: 2rem;
  font-weight: 500;
}

.v-card {
  max-width: 500px;
  margin: 0 auto;
}

.v-btn {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>

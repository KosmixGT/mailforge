<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-12">
          <v-card-text class="text-center">
            <v-icon color="error" size="64">mdi-alert-circle-outline</v-icon>
            <h1 class="headline">Страница не найдена!</h1>
            <p class="mt-4">Извините, страница, которую вы ищете, не найдена.</p>
            <p class="mt-4">Пожалуйста, попробуйте еще раз или перейдите на другую страницу</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" href="/" class="font-weight-bold">Перейти на главную</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style>
.mt-4{
  margin: 1px;
  font-size: 20px;
}

</style>

<template>
  <v-footer app class="bg-primary white--text">
    <v-container>
      <v-row justify="center">
        <v-col>
          <p class="footer-text mb-0">
            <strong>MailForge - Сервис рассылки сообщений по email и мессенджерам.</strong><br>
            <span>Мехоношин Константин</span>
            &copy; &nbsp;
            {{ new Date().getFullYear() }}
          </p>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
// Оставьте функции без изменений
</script>

<style scoped>
.bg-primary{
  height: 70px;
}
</style>

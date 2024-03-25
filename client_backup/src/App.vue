<template>
  <v-app>
    <the-header/>
    <v-main>
      <div class="main container">
        <router-view/>
      </div>
    </v-main>
    <the-footer/>
  </v-app>
</template>

<!-- <script setup>

</script> -->

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

html {
  overflow: auto !important;
}

</style>
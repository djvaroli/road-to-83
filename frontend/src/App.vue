<template>
  <div id="app" class="container">
    <CalorieDashboard></CalorieDashboard>
  </div>
</template>

<script>
import CalorieDashboard from "./components/CalorieDashboard";

export default {
  name: 'App',
  components: {
    CalorieDashboard
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'M PLUS Rounded 1c', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $text-color;
  margin-top: 60px;
}
</style>

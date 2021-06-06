<template>
  <div id="app" class="container">
    <b-tabs type="is-toggle">
      <b-tab-item label="Dashboard" icon="view-dashboard-outline">
        <template>
          <CalorieDashboard></CalorieDashboard>
        </template>
      </b-tab-item>
      <b-tab-item label="Interact" icon="chart-donut">
        <EntryInteractionComponent></EntryInteractionComponent>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import CalorieDashboard from "./components/CalorieDashboard";
import EntryInteractionComponent from "./components/EntryInteractionComponent";

export default {
  name: 'App',
  components: {
    CalorieDashboard, EntryInteractionComponent
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

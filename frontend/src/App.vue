<template>
  <div id="app" class="container">
    <b-tabs type="is-toggle">
      <b-tab-item label="Dashboard" icon="view-dashboard-outline">
        <template>
          <CalorieDashboard :data="data"></CalorieDashboard>
        </template>
      </b-tab-item>
      <b-tab-item label="Interact" icon="chart-donut">
        <EntryInteractionComponent @entry-update="fetchData"></EntryInteractionComponent>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import CalorieDashboard from "./components/CalorieDashboard";
import EntryInteractionComponent from "./components/EntryInteractionComponent";
import axios from "axios";

export default {
  name: 'App',
  components: {
    CalorieDashboard, EntryInteractionComponent
  },
  data() {
    return {
      data: {
        calorieSummaryData: {},
        series: [],
        chartOptions: {},
        history: []
      }
    }
  },
  methods: {
    fetchData() {
      const url = "http://127.0.0.1:8003/history/window_calories";
      const params = {
        windowSizeDays: 14
      }
      axios.get(url, {
        params: params
      })
      .then((response) => {
        this.data['calorieSummaryData'] = response.data.data['summary'];
        this.data['series'] = response.data.data.plot.series;
        this.data['chartOptions'] = response.data.data.plot.chartOptions;
        this.data['history'] = response.data.data.history.reverse();
      })
    }
  },
  mounted() {
    this.fetchData();
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

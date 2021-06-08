<template>
  <div id="app" class="container">
    <b-tabs type="is-toggle">
      <b-tab-item label="Calorie dashboard" icon="view-dashboard-outline">
        <template>
          <CalorieDashboard :data="calorieData"></CalorieDashboard>
        </template>
      </b-tab-item>
      <b-tab-item label="Weight dashboard" icon="view-dashboard-outline">
        <template>
          <WeightDashboard :data="weightData"></WeightDashboard>
        </template>
      </b-tab-item>
      <b-tab-item label="Interact" icon="chart-donut" v-if="showInteractTab">
        <EntryInteractionComponent @entry-update="fetchCalorieData"></EntryInteractionComponent>
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import CalorieDashboard from "./components/CalorieDashboard";
import EntryInteractionComponent from "./components/EntryInteractionComponent";
import WeightDashboard from "./components/WeightDashboard";

export default {
  name: 'App',
  components: {
    WeightDashboard,
    CalorieDashboard, EntryInteractionComponent
  },
  data() {
    return {
      calorieData: {
        calorieSummaryData: {},
        series: [],
        chartOptions: {},
        history: [],
      },
      weightData: {
        summary: {},
        series: [],
        chartOptions: {},
        history: []
      },
      showInteractTab: window.innerWidth > 1000
    }
  },
  methods: {
    fetchCalorieData() {
      const params = {
        windowSizeDays: 14
      }
      this.axios.get("/history/window_calories", {
        params: params
      })
      .then((response) => {
        this.calorieData['calorieSummaryData'] = response.data.data['summary'];
        this.calorieData['series'] = response.data.data.plot.series;
        this.calorieData['chartOptions'] = response.data.data.plot.chartOptions;
        this.calorieData['history'] = response.data.data.history.reverse();
      })
    },
    fetchWeightData() {
      const params = {
        windowSizeDays: 30
      }
      this.axios.get("/history/weight", {
        params: params
      })
      .then( (response) => {
        this.weightData = response.data;
      })
    }
  },
  mounted() {
    this.fetchCalorieData();
    this.fetchWeightData();
    window.onresize = () => {
      this.showInteractTab = window.innerWidth > 1000
    }
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
  margin-top: 20px;
}
</style>

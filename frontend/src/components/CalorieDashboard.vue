<template>
  <div class="calorie-dashboard">
    <div class="dashboard-row">
      <CalorieHistoryGraph :series="series" :chartOptions="chartOptions"></CalorieHistoryGraph>
    </div>
    <div class="dashboard-row">
      <CalorieHistoryTable :history="history"></CalorieHistoryTable>
      <CalorieSummaryTable :calorieSummaryData="calorieSummaryData"></CalorieSummaryTable>
    </div>
  </div>
</template>

<script>
import CalorieHistoryGraph from "./CalorieHistoryGraph";
import CalorieSummaryTable from "./CalorieSummaryTable";
import CalorieHistoryTable from "./CalorieHistoryTable";
import axios from "axios";

export default {
  name: "CalorieDashboard",
  components: {CalorieSummaryTable, CalorieHistoryGraph, CalorieHistoryTable},
  data () {
    return {
      series: [],
      chartOptions: {},
      calorieSummaryData: null,
      history: {}
    }
  },
  methods: {
    fetchGraphData() {
      const url = "http://127.0.0.1:8003/history/window_calories";
      const params = {
        windowSizeDays: 14
      }
      axios.get(url, {
        params: params
      })
      .then((response) => {
        console.log(response.data.data);
        this.calorieSummaryData = response.data.data['summary'];
        this.series = response.data.data.plot.series;
        this.chartOptions = response.data.data.plot.chartOptions;
        this.history = response.data.data.history.reverse();
      })
    }
  },
  mounted() {
    this.fetchGraphData()
  }
}
</script>

<style scoped lang="scss">
  .calorie-dashboard {
    display: flex;
    flex-direction: column;
  }

  .dashboard-row {
    display: flex;
    margin-bottom: 1rem;
    @media screen and (max-width: $mobile-screen-max-width) {
      flex-direction: column;
    }
  }
</style>

<template>
  <div class="calorie-dashboard">
    <CalorieHistoryGraph :series="series" :chartOptions="chartOptions"></CalorieHistoryGraph>
    <CalorieSummaryTable :calorieSummaryData="calorieSummaryData"></CalorieSummaryTable>
  </div>
</template>

<script>
import CalorieHistoryGraph from "./CalorieHistoryGraph";
import CalorieSummaryTable from "./CalorieSummaryTable";
import axios from "axios";

export default {
  name: "CalorieDashboard",
  components: {CalorieSummaryTable, CalorieHistoryGraph},
  data () {
    return {
      series: [],
      chartOptions: {},
      calorieSummaryData: null
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
        this.calorieSummaryData = response.data.data['summary'];
        this.series = response.data.data.plot.series;
        this.chartOptions = response.data.data.plot.chartOptions;
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
  }
</style>

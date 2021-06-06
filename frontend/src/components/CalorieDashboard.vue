<template>
  <div class="calorie-dashboard">
    <div class="dashboard-row">
      <CalorieHistoryGraph :series="data.series" :chartOptions="data.chartOptions"></CalorieHistoryGraph>
    </div>
    <div class="dashboard-row">
      <CalorieSummaryTable :calorieSummaryData="data.calorieSummaryData"></CalorieSummaryTable>
      <CalorieHistoryTable :history="data.history"></CalorieHistoryTable>
    </div>
  </div>
</template>

<script>
import CalorieHistoryGraph from "./CalorieHistoryGraph";
import CalorieSummaryTable from "./CalorieSummaryTable";
import CalorieHistoryTable from "./CalorieHistoryTable";

export default {
  name: "CalorieDashboard",
  components: {CalorieSummaryTable, CalorieHistoryGraph, CalorieHistoryTable},
  props: ["data"],
  data () {
    return {
    }
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

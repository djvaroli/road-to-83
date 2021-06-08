<template>
  <div class="weight-dashboard">
    <div class="dashboard-row">
      <WeightHistoryGraph :series="data.series" :chartOptions="data.chartOptions"></WeightHistoryGraph>
    </div>
    <div class="dashboard-row">
      <WeightHistoryTable :history="data.history"></WeightHistoryTable>
    </div>
  </div>
</template>

<script>
import WeightHistoryGraph from "./WeightHistoryGraph";
import WeightHistoryTable from "./WeightHistoryTable";
export default {
  name: "WeightDashboard",
  components: {WeightHistoryTable, WeightHistoryGraph},
  props: ["data"],
}
</script>

<style scoped>

</style>

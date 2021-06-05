<template>
  <div id="chart" class="chart">
    <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
  name: "CalorieHistoryGraph",
  props: [
      "series",
      "chartOptions"
  ],
  data () {
    return {
    }
  }
}
</script>

<style scoped>

</style>

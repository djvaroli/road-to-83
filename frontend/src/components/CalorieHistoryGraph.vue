<template>
  <div id="calorie-summary-figure" class="figure flex-item-space-right">
    <div class="plot">
      <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
    </div>
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

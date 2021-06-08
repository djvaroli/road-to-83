<template>
  <div id="weight-history-figure" class="figure flex-item-space-right">
    <div class="plot">
      <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
    </div>
  </div>
</template>

<script>
export default {
  name: "WeightHistoryGraph",
  props: ["series", "chartOptions"]
}
</script>

<style scoped>

</style>

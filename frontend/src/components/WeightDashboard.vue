<template>
  <div id="weight-history-figure" class="figure flex-item-space-right">
    <div class="plot">
      <apexchart type="line" height="350" :options="data.chartOptions" :series="data.series"></apexchart>
    </div>
  </div>
</template>

<script>
export default {
  name: "WeightDashboard",
  props: ["data"],
  mounted () {
    console.log(this.data);
  }
}
</script>

<style scoped>

</style>

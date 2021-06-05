<template>
  <div id="calorie-summary-table" class="summary-table align-items-left">
    <div class="summary-table-header"><b>Summary</b></div>
    <div class="summary-table-content">
      <b>Maintenance calories:</b> {{ calorieSummaryData.average_daily_maintenance_calories }}
      <br>
      <b>Goal calories:</b> {{ calorieSummaryData.average_daily_calorie_need }}
      <br>
      <b>Daily average calories:</b> {{ calorieSummaryData.average_daily_calories }}
      <br>
      <b>Difference to goal:</b> {{ calorieSummaryData.average_daily_difference }}
      <br>
      <b>Daily average caloric deficit:</b> {{ calorieSummaryData.average_daily_caloric_deficit }}
      <br>
      <b>Net caloric deficit:</b> {{ calorieSummaryData.net_calorie_deficit }}
    </div>
  </div>
</template>

<script>
export default {
  name: "CalorieSummaryTable",
  props: ["calorieSummaryData"],
  data () {
    return {
    }
  }
}
</script>

<style scoped lang="scss">
</style>

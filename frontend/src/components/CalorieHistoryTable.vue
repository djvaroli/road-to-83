<template>
  <div id="calorie-history-table">
    <b-table
        :data="history"
        :hoverable="true"
        :mobile-cards="true"
        :paginated="true"
        :per-page="5"
    >
      <b-table-column field="display_date" label="Date" v-slot="props">
        {{ props.row.display_date }}
      </b-table-column>

      <b-table-column field="calories" label="Calories" v-slot="props" :numeric="true">
        {{ props.row.calories }}
      </b-table-column>

      <b-table-column  field="id" label="Entry ID" v-slot="props">
        {{ props.row.id }}
      </b-table-column>

      <template #empty>
        <div class="has-text-centered">No records</div>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  name: "CalorieHistoryTable",
  props: ["history"],
  data() {
    return {
      columns: [
        {
          field: 'calories',
          label: 'Calories',
          numeric: true
        },
        {
          field: 'display_date',
          label: 'Date',
          centered: true
        }
      ]
    }
  }
}
</script>

<style scoped lang="scss">
  #calorie-history-table {
    @include bordered-dashboard-card;
    margin-left: 1rem;
    @media screen and (max-width: $mobile-screen-max-width) {
      margin-left: 0;
    }
  }

</style>

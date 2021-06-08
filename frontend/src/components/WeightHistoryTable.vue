<template>
  <div id="weight-history-table">
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
        {{ props.row.weight }}
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
  name: "WeightHistoryTable",
  props: ["history"],
  data() {
    return {
    }
  }
}
</script>

<style scoped lang="scss">
  #weight-history-table {
    @include bordered-dashboard-card;
    @media screen and (max-width: $mobile-screen-max-width) {
      margin-left: 0;
    }
  }

</style>

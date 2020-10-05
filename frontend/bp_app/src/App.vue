<template>
  <div id="app">
    <Records v-bind:records="records"/>
  </div>
</template>

<script>
import Records from "./components/Records"

export default {
  name: 'App',
  components: {
    Records
  },
  data () {
    return {
      records: [
        {
          record_id: 549,
          timestamp: "2020-10-05T09:23:52Z",
          bp_upper: 156,
          bp_lower: 63,
          notes: "Test"
        },
        {
          record_id: 550,
          timestamp: "2020-10-04T09:23:52Z",
          bp_upper: 160,
          bp_lower: 60,
          notes: "Test"
        }
      ]
    }
  }
}
</script>

<style>
</style>

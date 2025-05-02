<template>
  <div>
    <h3 class="text-xl font-semibold text-neutral my-6">Data Table</h3>

    <div class="overflow-x-auto rounded-box border border-base-content/5 bg-base-100">
      <table class="table">
        <thead>
          <tr>
            <th>{{ periodLabel }}</th>
            <th>Streams</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data" :key="index">
            <td>{{ getItemDate(item) }}</td>
            <td>{{ item.streams?.toLocaleString() }}</td>
          </tr>
          <tr v-if="data.length === 0">
            <td colspan="2">
              No data available
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  timePeriod: {
    type: String,
    default: 'monthly'
  }
})

// Computed
const periodLabel = computed(() => {
  if (props.timePeriod === 'daily') return 'Date'
  if (props.timePeriod === 'weekly') return 'Week'
  return 'Month'
})

// Methods
const getItemDate = (item) => {
  if (props.timePeriod === 'daily') return item.date
  if (props.timePeriod === 'weekly') return `Week ${item.week}`
  return item.month
}
</script>

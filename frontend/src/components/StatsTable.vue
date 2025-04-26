<template>
  <div class="bg-white rounded-lg shadow-sm p-5">
    <h3 class="text-lg font-medium text-gray-800 mb-4">Data Table</h3>
    
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ periodLabel }}
            </th>
            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Streams
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(item, index) in data" :key="index" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ getItemDate(item) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ item.streams?.toLocaleString() }}
            </td>
          </tr>
          <tr v-if="data.length === 0">
            <td colspan="2" class="px-6 py-4 text-center text-sm text-gray-500 italic">
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

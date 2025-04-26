<template>
  <div class="bg-white rounded-lg shadow-sm p-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h2 class="font-semibold text-xl text-gray-800 truncate">{{ filename }}</h2>
      </div>
      
      <button 
        @click="$emit('back')" 
        class="flex items-center gap-1 text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1.5 rounded transition"
      >
        <span>←</span> Back to Files
      </button>
    </div>
    
    <div class="mt-5 p-4 bg-gray-50 rounded-lg">
      <div class="flex flex-wrap gap-4 items-end">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Time Period:</label>
          <select 
            v-model="localTimePeriod"
            class="bg-white border border-gray-300 rounded px-3 py-2 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Store:</label>
          <select 
            v-model="localStore"
            class="bg-white border border-gray-300 rounded px-3 py-2 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Stores</option>
            <option v-for="store in availableStores" :key="store" :value="store">
              {{ store }}
            </option>
          </select>
        </div>
        
        <button 
          @click="applyFilters"
          class="bg-blue-600 text-white py-2 px-4 rounded font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Apply Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  filename: {
    type: String,
    required: true
  },
  timePeriod: {
    type: String,
    default: 'monthly'
  },
  selectedStore: {
    type: String,
    default: ''
  },
  availableStores: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['back', 'filters-updated'])

// Local state for form controls
const localTimePeriod = ref(props.timePeriod)
const localStore = ref(props.selectedStore)

// Watch for prop changes to update local state
watch(() => props.timePeriod, (newValue) => {
  localTimePeriod.value = newValue
})

watch(() => props.selectedStore, (newValue) => {
  localStore.value = newValue
})

// Methods
const applyFilters = () => {
  emit('filters-updated', {
    timePeriod: localTimePeriod.value,
    store: localStore.value
  })
}
</script>

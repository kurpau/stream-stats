<template>
  <div class="card shadow-sm p-3">
    <div class="flex justify-between items-center mb-2">
      <div class="badge">
        <h2 class="text-base">{{ filename }}</h2>
      </div>

      <button 
        @click="$emit('back')" 
        class="btn"
      >
        <span>←</span> Back to Files
      </button>
    </div>

    <div class="card bg-base-200 p-3 flex-row justify-between gap-2">
      <div class="flex gap-2">
        <fieldset class="fieldset">
          <legend class="fieldset-legend">Time Period:</legend>
          <select 
            v-model="localTimePeriod"
            class="select"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </fieldset>

        <fieldset class="fieldset">
          <legend class="fieldset-legend">Store:</legend>
          <select 
            v-model="localStore"
            class="select"
          >
            <option value="">All Stores</option>
            <option v-for="store in availableStores" :key="store" :value="store">
              {{ store }}
            </option>
          </select>
        </fieldset>
      </div>

      <button 
        @click="applyFilters"
        class="btn btn-primary self-end my-1"
      >
        Apply Filters
      </button>
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

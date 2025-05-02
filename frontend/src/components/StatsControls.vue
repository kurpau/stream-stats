<template>
  <div class="card shadow-sm p-3">
    <div class="flex justify-between items-center mb-2">
      <div class="badge">
        <h2 class="text-base">{{ filename }}</h2>
      </div>

      <button @click="$emit('back')" class="btn">
        <span>←</span> Back to Files
      </button>
    </div>

    <div class="card bg-base-200 p-3 flex-row gap-4 flex-wrap">

      <fieldset class="fieldset">
        <legend class="fieldset-legend">Store</legend>
        <select v-model="localStore" class="select">
          <option value="">All Stores</option>
          <option v-for="store in availableStores" :key="store" :value="store">{{ store }}</option>
        </select>
      </fieldset>

      <fieldset class="fieldset">
        <legend class="fieldset-legend">Year</legend>
        <select v-model="localYear" class="select">
          <option value="">All Years</option>
          <option v-for="year in availableYears" :key="year" :value="year.toString()">{{ year }}</option>
        </select>
      </fieldset>

      <fieldset class="fieldset">
        <legend class="fieldset-legend">Month</legend>
        <select v-model="localMonth" class="select">
          <option value="">All Months</option>
          <option v-for="month in availableMonths" :key="month.key" :value="month.key.toString()">{{ month.name }}</option>
        </select>
      </fieldset>

      <fieldset class="fieldset">
        <legend class="fieldset-legend">Country</legend>
        <select v-model="localCountry" class="select">
          <option value="">All Countries</option>
          <option v-for="country in availableCountries" :key="country.key" :value="country.key">
            {{ country.name }}
          </option>
        </select>
      </fieldset>
    </div>

    <div class="flex justify-between mt-4">
      <button @click="resetFilters" class="btn">Reset Filters</button>
      <button @click="applyFilters" class="btn btn-primary">Apply Filters</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  filename: String,
  selectedStore: String,
  selectedYear: String,
  selectedMonth: String,
  selectedCountry: String,
  availableStores: Array,
  availableYears: Array,
  availableMonths: Array,
  availableCountries: Array
})

const emit = defineEmits(['back', 'filters-updated', 'reset-filters'])

const localStore = ref(props.selectedStore)
const localYear = ref(props.selectedYear)
const localMonth = ref(props.selectedMonth)
const localCountry = ref(props.selectedCountry)

watch(() => props.selectedStore, (val) => localStore.value = val)
watch(() => props.selectedYear, (val) => localYear.value = val)
watch(() => props.selectedMonth, (val) => localMonth.value = val)
watch(() => props.selectedCountry, (val) => localCountry.value = val)

const applyFilters = () => {
  emit('filters-updated', {
    store: localStore.value,
    year: localYear.value,
    month: localMonth.value,
    country: localCountry.value
  })
}

const resetFilters = () => {
  localStore.value = ''
  localYear.value = ''
  localMonth.value = ''
  localCountry.value = ''
  emit('reset-filters')
}
</script>

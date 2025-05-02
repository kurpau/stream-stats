<template>
  <section class="container mx-auto px-4 py-8 max-w-6xl">
    <h1 class="text-3xl font-bold text-center mb-8">Stream Stats</h1>

    <FileUploader 
      v-if="!selectedFile" 
      :available-files="availableFiles" 
      @file-selected="handleFileSelect" 
      @file-uploaded="handleFileUpload"
      class="max-w-xl mx-auto"
    />
    
    <div v-else class="w-full">
      <StatsControls 
        :filename="selectedFile"
        :selected-store="selectedStore"
        :selected-year="selectedYear"
        :selected-month="selectedMonth"
        :selected-country="selectedCountry"
        :available-stores="stats.filters?.available_stores || []"
        :available-years="stats.filters?.available_years || []"
        :available-months="stats.filters?.available_months || []"
        :available-countries="stats.filters?.available_countries || []"
        @back="goBack"
        @filters-updated="updateFilters"
        @reset-filters="resetFilters"
        class="mb-6"
      />
      
      <StatsSummary 
        :stats="stats" 
        class="mb-8"
      />
      
      <StatsTable 
        :data="stats.data" 
        class="w-full" 
      />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import FileUploader from './components/FileUploader.vue'
import StatsControls from './components/StatsControls.vue'
import StatsSummary from './components/StatsSummary.vue'
import StatsTable from './components/StatsTable.vue'

const selectedFile = ref(null)
const availableFiles = ref([])
const stats = ref({})
const selectedStore = ref('')
const selectedYear = ref('')
const selectedMonth = ref('')
const selectedCountry = ref('')
const apiUrl = 'http://localhost:8000'

const defaultsApplied = ref(false)

const fetchAvailableFiles = async () => {
  try {
    const response = await fetch(`${apiUrl}/available-files/`)
    const data = await response.json()
    availableFiles.value = data.files
  } catch (error) {
    console.error('Error fetching files:', error)
    alert('Error fetching available files. Make sure backend is running.')
  }
}

const fetchStats = async () => {
  if (!selectedFile.value) return
  
  try {
    const url = new URL(`${apiUrl}/streaming-stats/`)
    url.searchParams.append('filename', selectedFile.value)
    url.searchParams.append('store', selectedStore.value || 'any')
    url.searchParams.append('year', selectedYear.value || 'any')
    url.searchParams.append('month', selectedMonth.value || 'any')
    url.searchParams.append('country', selectedCountry.value || 'any')

    const response = await fetch(url)
    stats.value = await response.json()

    if (!defaultsApplied.value) {

      if (!selectedStore.value && stats.value.filters?.available_stores.includes('Spotify')) {
        selectedStore.value = 'Spotify'
      }

      if (!selectedYear.value) {
        selectedYear.value = new Date().getFullYear().toString()
      }

      if (!selectedMonth.value) {
        const today = new Date()
        let defaultMonth = today.getMonth() - 2
        if (defaultMonth <= 0) {
          defaultMonth = 12 + defaultMonth
        }
        selectedMonth.value = defaultMonth.toString()
      }

      defaultsApplied.value = true

      fetchStats()
    }

  } catch (error) {
    console.error('Error fetching stats:', error)
    alert('Error fetching statistics. Make sure backend is running.')
  }
}

const handleFileSelect = (filename) => {
  selectedFile.value = filename
  fetchStats()
}

const handleFileUpload = (filename) => {
  selectedFile.value = filename
  fetchStats()
  fetchAvailableFiles()
}

const updateFilters = (filters) => {
  selectedStore.value = filters.store
  selectedYear.value = filters.year
  selectedMonth.value = filters.month
  selectedCountry.value = filters.country
  fetchStats()
}

const resetFilters = () => {
  selectedStore.value = ''
  selectedYear.value = ''
  selectedMonth.value = ''
  selectedCountry.value = ''
  fetchStats()
}

const goBack = () => {
  selectedFile.value = null
  stats.value = {}
}

onMounted(() => {
  fetchAvailableFiles()
})
</script>

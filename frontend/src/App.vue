<template>
  <section>
    <h1 class="btn">Stream Stats</h1>
    
    <FileUploader 
      v-if="!selectedFile" 
      :available-files="availableFiles" 
      @file-selected="handleFileSelect" 
      @file-uploaded="handleFileUpload"
    />
    
    <div v-else>
      <StatsControls 
        :filename="selectedFile"
        :time-period="timePeriod"
        :selected-store="selectedStore"
        :available-stores="stats.available_stores"
        @back="goBack"
        @filters-updated="updateFilters"
      />
      
      <StatsSummary :stats="stats" />
      
      <StatsTable 
        :data="stats.data" 
        :time-period="timePeriod" 
      />
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import FileUploader from './components/FileUploader.vue'
import StatsControls from './components/StatsControls.vue'
import StatsSummary from './components/StatsSummary.vue'
import StatsTable from './components/StatsTable.vue'

// State
const selectedFile = ref(null)
const availableFiles = ref([])
const stats = ref({
  data: [],
  available_stores: []
})
const timePeriod = ref('monthly')
const selectedStore = ref('')
const apiUrl = 'http://localhost:8000'

// Methods
const fetchAvailableFiles = async () => {
  try {
    const response = await fetch(`${apiUrl}/available-files/`)
    const data = await response.json()
    availableFiles.value = data.files
  } catch (error) {
    console.error('Error fetching files:', error)
    alert('Error fetching available files. Make sure the backend server is running.')
  }
}

const fetchStats = async () => {
  if (!selectedFile.value) return
  
  try {
    const url = new URL(`${apiUrl}/streaming-stats/`)
    url.searchParams.append('filename', selectedFile.value)
    url.searchParams.append('time_period', timePeriod.value)
    
    if (selectedStore.value) {
      url.searchParams.append('store', selectedStore.value)
    }
    
    const response = await fetch(url)
    stats.value = await response.json()
  } catch (error) {
    console.error('Error fetching stats:', error)
    alert('Error fetching statistics. Make sure the backend server is running.')
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

const updateFilters = ({ timePeriod: newTimePeriod, store: newStore }) => {
  timePeriod.value = newTimePeriod
  selectedStore.value = newStore
  fetchStats()
}

const goBack = () => {
  selectedFile.value = null
  stats.value = {
    data: [],
    available_stores: []
  }
}

// Lifecycle
onMounted(() => {
  fetchAvailableFiles()
})
</script>

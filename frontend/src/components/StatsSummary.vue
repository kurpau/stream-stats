<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="bg-white rounded-lg shadow-sm p-5">
      <h3 class="text-sm font-medium text-gray-500 mb-1">Total Streams</h3>
      <div class="text-2xl font-bold text-blue-600">
        {{ stats.total_streams?.toLocaleString() || 0 }}
      </div>
    </div>
    
    <!-- Additional summary cards can be added here as the app grows -->
  </div>
</template>

<script setup>
// Props
defineProps({
  stats: {
    type: Object,
    required: true
  }
})
</script>

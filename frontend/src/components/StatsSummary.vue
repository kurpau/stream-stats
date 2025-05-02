<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Streams</h3>
        <div class="text-info text-xl font-bold">
          {{ stats.streams?.toLocaleString() || 0 }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    required: true
  }
})
</script>

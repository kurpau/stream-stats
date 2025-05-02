<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Streams</h3>
        <div class="text-info text-xl font-bold">
          {{ stats.streams.toLocaleString() || 0 }}
        </div>
      </div>
    </div>
    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Earnings</h3>
        <div class="text-info text-xl font-bold">
          {{ stats.earnings.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) || '$0.00' }}
        </div>
      </div>
    </div>
    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Pay Per Stream</h3>
        <div class="text-info text-xl font-bold">
          {{ (stats.earnings/stats.streams).toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 3 }) || '$0.000' }}
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

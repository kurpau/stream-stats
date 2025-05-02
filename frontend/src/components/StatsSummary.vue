<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">

    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Streams</h3>
        <div class="text-info text-xl font-bold">
          {{ formattedStreams }}
        </div>
      </div>
    </div>

    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Earnings</h3>
        <div class="text-info text-xl font-bold">
          {{ formattedEarnings }}
        </div>
      </div>
    </div>

    <div class="card card-border card-md shadow-sm">
      <div class="card-body items-center">
        <h3 class="card-title">Pay Per Stream</h3>
        <div class="text-info text-xl font-bold">
          {{ payPerStream }}
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    required: true
  }
})

const formattedStreams = computed(() => {
  const streams = props.stats.streams ?? 0
  return streams.toLocaleString()
})

const formattedEarnings = computed(() => {
  const earnings = props.stats.earnings ?? 0
  return earnings.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
})

const payPerStream = computed(() => {
  const streams = props.stats.streams ?? 0
  const earnings = props.stats.earnings ?? 0
  const result = streams ? earnings / streams : 0

  return isFinite(result)
    ? result.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 3 })
    : '$0.000'
})
</script>

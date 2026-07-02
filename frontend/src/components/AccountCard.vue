<template>
  <div
    class="relative overflow-hidden rounded-2xl p-6 text-white shadow-xl transition-all duration-300
           hover:-translate-y-1 hover:shadow-2xl cursor-default select-none"
    :style="cardStyle"
    role="region"
    :aria-label="`${title}: ${formatCurrency(balance)}`"
  >
    <!-- Decorative blobs -->
    <div class="absolute -right-10 -top-10 w-40 h-40 rounded-full bg-white opacity-[0.06]"></div>
    <div class="absolute right-6 -bottom-12 w-32 h-32 rounded-full bg-white opacity-[0.06]"></div>

    <div class="flex justify-between items-start mb-6">
      <div>
        <p class="text-sm font-semibold opacity-90 tracking-wide">{{ title }}</p>
        <p class="text-xs opacity-60 mt-0.5">{{ accountType }}</p>
      </div>
      <div class="w-11 h-11 rounded-xl bg-white/20 flex items-center justify-center text-xl backdrop-blur-sm border border-white/10">
        {{ icon }}
      </div>
    </div>

    <div class="mb-5">
      <p class="text-[2rem] font-extrabold tracking-tight tabular-nums leading-none">
        {{ formatCurrency(balance) }}
      </p>
      <p class="text-xs opacity-60 mt-1.5 uppercase tracking-widest font-medium">Available Balance</p>
    </div>

    <div class="flex items-center justify-between">
      <span class="text-xs px-3 py-1 rounded-full bg-white/15 font-mono tracking-widest border border-white/10">
        {{ accountNumber }}
      </span>
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span>
        <span class="text-xs opacity-70 font-medium">Active</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title:         { type: String, required: true },
  accountType:   { type: String, required: true },
  icon:          { type: String, required: true },
  balance:       { type: Number, required: true },
  gradient:      { type: Array,  required: true },
  accountNumber: { type: String, required: true },
})

const cardStyle = computed(() => ({
  background: `linear-gradient(135deg, ${props.gradient[0]} 0%, ${props.gradient[1]} 100%)`,
}))

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency', currency: 'INR', maximumFractionDigits: 0,
  }).format(value)
}
</script>

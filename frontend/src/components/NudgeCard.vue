<template>
  <div class="space-y-4">
    <!-- AI chat bubble -->
    <div class="flex items-start gap-2.5">
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-500
                  flex items-center justify-center text-sm flex-shrink-0 mt-0.5 shadow-sm"
           aria-hidden="true">
        🤖
      </div>

      <div class="bg-slate-50 rounded-2xl rounded-tl-sm px-4 py-3.5 flex-1 border border-slate-100 shadow-xs">
        <div class="space-y-2">
          <p v-for="(para, i) in paragraphs" :key="i" class="text-slate-700 text-sm leading-relaxed">
            {{ para }}
          </p>
        </div>

        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center gap-3 flex-wrap">
          <span class="text-xs px-2.5 py-1 rounded-full font-semibold" :class="actionBadgeClass">
            {{ actionLabel }}
          </span>
          <span class="text-xs text-slate-400">
            Suggested: <strong class="text-slate-700 font-semibold">{{ formatCurrency(nudge.amount) }}</strong>
          </span>
        </div>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="flex gap-3 pl-10">
      <button
        class="btn-primary flex-1 text-sm"
        :disabled="loading"
        @click="$emit('execute', nudge.id)"
        :aria-label="`Accept recommendation: ${actionLabel} for ${formatCurrency(nudge.amount)}`"
        :aria-busy="loading"
      >
        <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" aria-hidden="true"></span>
        <span>{{ loading ? 'Processing…' : '✅ Yes, execute this' }}</span>
      </button>

      <button
        class="btn-ghost text-sm px-4"
        :disabled="loading"
        @click="$emit('dismiss', nudge.id)"
        aria-label="Dismiss this AI recommendation for now"
      >
        Not now
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  nudge:   { type: Object,  required: true },
  loading: { type: Boolean, default: false },
})

defineEmits(['execute', 'dismiss'])

const paragraphs = computed(() =>
  (props.nudge?.message || '').split('\n\n').filter(Boolean)
)

const ACTION_LABELS = {
  invest_liquid_fund: '📈 SBI Liquid Fund',
  create_fd:          '🔒 Fixed Deposit',
  invest_mf:          '📊 Mutual Fund',
}

const ACTION_BADGE_CLASSES = {
  invest_liquid_fund: 'bg-blue-50 text-blue-700',
  create_fd:          'bg-amber-50 text-amber-700',
  invest_mf:          'bg-violet-50 text-violet-700',
}

const actionLabel     = computed(() => ACTION_LABELS[props.nudge?.proposed_action] || '💰 Investment')
const actionBadgeClass = computed(() => ACTION_BADGE_CLASSES[props.nudge?.proposed_action] || 'bg-violet-50 text-violet-700')

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency', currency: 'INR', maximumFractionDigits: 0,
  }).format(value)
}
</script>

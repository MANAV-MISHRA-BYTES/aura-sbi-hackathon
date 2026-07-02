<template>
  <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">

    <!-- Expanded nudge panel -->
    <Transition name="panel">
      <div
        v-if="isOpen"
        class="w-[340px] sm:w-[380px] rounded-2xl shadow-2xl overflow-hidden border border-slate-100"
        role="dialog" aria-modal="true" aria-label="Aura AI Financial Recommendation" id="aura-panel"
      >
        <div class="bg-gradient-to-r from-violet-600 to-indigo-600 px-4 py-3 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 bg-white/20 rounded-full flex items-center justify-center border border-white/20">
              <span class="text-base" aria-hidden="true">🤖</span>
            </div>
            <div>
              <p class="text-white text-sm font-bold leading-tight">Aura AI Agent</p>
              <div class="flex items-center gap-1.5 mt-0.5">
                <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" aria-hidden="true"></span>
                <span class="text-white/70 text-xs">Analysed your finances</span>
              </div>
            </div>
          </div>
          <button @click="close"
                  class="text-white/70 hover:text-white transition-colors p-1.5 rounded-lg hover:bg-white/15
                         focus:outline-none focus:ring-2 focus:ring-white/50"
                  aria-label="Close Aura panel">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="bg-white px-4 py-4">
          <NudgeCard
            v-if="currentNudge"
            :nudge="currentNudge"
            :loading="executing"
            @execute="handleExecute"
            @dismiss="handleDismiss"
          />
          <div v-else class="py-6 text-center">
            <span class="text-4xl block mb-2" aria-hidden="true">🎯</span>
            <p class="text-slate-700 font-semibold text-sm">All clear!</p>
            <p class="text-slate-400 text-xs mt-1 leading-relaxed">No pending recommendations.<br>Aura is watching your finances.</p>
          </div>
        </div>

        <Transition name="fade">
          <div v-if="successMessage" class="bg-emerald-50 border-t border-emerald-100 px-4 py-3" role="status" aria-live="polite">
            <div class="flex items-center gap-2 text-emerald-700">
              <span class="text-lg" aria-hidden="true">✅</span>
              <p class="text-sm font-semibold">{{ successMessage }}</p>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>

    <!-- Floating action button -->
    <button
      @click="toggle"
      class="relative w-14 h-14 rounded-full shadow-xl flex items-center justify-center
             transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-violet-300 focus:ring-offset-2"
      :class="isOpen
        ? 'bg-slate-700 hover:bg-slate-800'
        : 'bg-gradient-to-br from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 aura-pulse'"
      :aria-label="isOpen ? 'Close Aura AI assistant' : 'Open Aura AI assistant'"
      :aria-expanded="isOpen"
      :aria-controls="isOpen ? 'aura-panel' : undefined"
    >
      <Transition name="icon-swap" mode="out-in">
        <span v-if="isOpen"  class="text-white text-xl" key="close" aria-hidden="true">✕</span>
        <span v-else class="text-2xl" key="bot" aria-hidden="true">🤖</span>
      </Transition>

      <!-- Notification badge -->
      <span
        v-if="!isOpen && nudges.length > 0"
        class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full
               flex items-center justify-center text-white text-[10px] font-bold shadow-md animate-bounce"
        :aria-label="`${nudges.length} new AI recommendation${nudges.length > 1 ? 's' : ''}`"
        role="status"
      >
        {{ nudges.length }}
      </span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import NudgeCard from './NudgeCard.vue'
import { executeNudge, dismissNudge } from '../api/index.js'

const props = defineProps({ nudges: { type: Array, default: () => [] } })
const emit  = defineEmits(['nudge-accepted', 'nudge-dismissed'])

const isOpen         = ref(false)
const executing      = ref(false)
const successMessage = ref('')

const currentNudge = computed(() => props.nudges[0] ?? null)

// Auto-open panel when the first nudge arrives
watch(
  () => props.nudges.length,
  (newLen, oldLen) => { if (newLen > 0 && oldLen === 0) isOpen.value = true }
)

function toggle() { isOpen.value = !isOpen.value; if (!isOpen.value) successMessage.value = '' }
function close()  { isOpen.value = false; successMessage.value = '' }

async function handleExecute(nudgeId) {
  executing.value = true
  try {
    const { data } = await executeNudge(nudgeId)
    successMessage.value = data.message
    emit('nudge-accepted', data)
    setTimeout(() => { successMessage.value = ''; isOpen.value = false }, 3000)
  } catch (err) {
    console.error('[Aura] Execute failed:', err)
  } finally {
    executing.value = false
  }
}

async function handleDismiss(nudgeId) {
  try {
    await dismissNudge(nudgeId)
    emit('nudge-dismissed')
    close()
  } catch (err) {
    console.error('[Aura] Dismiss failed:', err)
  }
}
</script>

<style scoped>
.panel-enter-active { animation: panelIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }
.panel-leave-active { animation: panelIn 0.2s ease-in reverse; }
@keyframes panelIn {
  from { opacity: 0; transform: translateY(20px) scale(0.96); }
  to   { opacity: 1; transform: translateY(0)    scale(1);    }
}

.icon-swap-enter-active, .icon-swap-leave-active { transition: all 0.15s ease; }
.icon-swap-enter-from, .icon-swap-leave-to       { opacity: 0; transform: scale(0.5); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }

/* Pulsing glow ring on FAB when idle */
.aura-pulse { animation: auraPulse 2.5s ease-in-out infinite; }
@keyframes auraPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(124,58,237,0.5), 0 10px 30px rgba(124,58,237,0.35); }
  50%       { box-shadow: 0 0 0 10px rgba(124,58,237,0), 0 10px 30px rgba(124,58,237,0.5); }
}
</style>

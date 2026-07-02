<template>
  <div class="min-h-screen bg-slate-50">

    <!-- Skip to main content (WCAG 2.1 §2.4.1) -->
    <a href="#main-content"
       class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2
              focus:z-50 focus:bg-white focus:px-4 focus:py-2 focus:rounded-lg focus:shadow-lg
              focus:text-sbi-deep focus:font-semibold text-sm">
      Skip to main content
    </a>

    <!-- Header -->
    <header class="bg-sbi-deep text-white shadow-2xl sticky top-0 z-10" role="banner">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        <div class="flex items-center gap-3 flex-shrink-0">
          <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-sm">
            <span class="text-sbi-deep font-black text-base tracking-tight leading-none">SBI</span>
          </div>
          <div class="hidden sm:block">
            <p class="font-bold text-base leading-tight">State Bank of India</p>
            <p class="text-[11px] text-sky-300 leading-tight font-medium tracking-wide">YONO — Next Generation</p>
          </div>
        </div>

        <div class="hidden md:flex items-center gap-2 bg-white/10 px-4 py-1.5 rounded-full border border-white/20 backdrop-blur-sm"
             role="status" aria-label="Aura AI agent is active">
          <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" aria-hidden="true"></span>
          <span class="text-sm font-bold tracking-widest text-white">AURA</span>
          <span class="text-xs text-white/60 font-medium">AI Agent Active</span>
        </div>

        <div class="flex items-center gap-3 flex-shrink-0">
          <div class="text-right hidden sm:block">
            <p class="text-sm font-semibold leading-tight">{{ user?.name ?? '—' }}</p>
            <p class="text-xs text-sky-300 leading-tight">Retail Customer</p>
          </div>
          <div class="w-9 h-9 rounded-full bg-sbi-sky flex items-center justify-center
                      text-sm font-bold border-2 border-white/30 shadow"
               :aria-label="`User: ${user?.name ?? 'Loading'}`">
            {{ user?.name?.charAt(0) ?? 'R' }}
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main id="main-content" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" role="main">

      <!-- Greeting -->
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-tight">
          Good {{ timeOfDay }}, <span class="text-sbi-sky">{{ firstName }}</span>
          <span aria-hidden="true"> 👋</span>
        </h1>
        <p class="text-slate-500 mt-1.5 text-sm sm:text-base">
          Here's your financial snapshot —
          <time :datetime="isoDate" class="font-medium text-slate-600">{{ formattedDate }}</time>
        </p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-28" role="status" aria-label="Loading dashboard">
        <div class="w-14 h-14 border-4 border-sbi-deep border-t-transparent rounded-full animate-spin mb-4"></div>
        <p class="text-slate-500 font-medium text-sm">Loading your dashboard…</p>
      </div>

      <template v-else>

        <!-- Account balance cards -->
        <section aria-label="Account balances" class="mb-8">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <AccountCard title="Checking Account" account-type="SBI Current Account" icon="💳"
                         :balance="user?.checking_balance ?? 0" :gradient="['#003478', '#002456']"
                         account-number="XXXX XXXX 4821" />
            <AccountCard title="Savings Account"  account-type="SBI Savings Plus"    icon="🏦"
                         :balance="user?.savings_balance ?? 0"  :gradient="['#0072BC', '#005fa3']"
                         account-number="XXXX XXXX 9034" />
          </div>
        </section>

        <!-- Aura agent trigger -->
        <section class="mb-8 rounded-2xl bg-gradient-to-r from-violet-600 to-indigo-600
                        p-6 shadow-lg text-white relative overflow-hidden"
                 aria-label="Aura AI Financial Agent">
          <div class="absolute right-0 top-0 w-48 h-48 rounded-full bg-white/5 -translate-y-1/2 translate-x-1/4" aria-hidden="true"></div>
          <div class="absolute left-1/3 bottom-0 w-32 h-32 rounded-full bg-white/5 translate-y-1/2" aria-hidden="true"></div>

          <div class="relative flex flex-col sm:flex-row items-start sm:items-center justify-between gap-5">
            <div>
              <h2 class="text-lg font-bold flex items-center gap-2"><span aria-hidden="true">🤖</span> Aura Financial AI</h2>
              <p class="text-violet-200 text-sm mt-1.5 leading-relaxed max-w-sm">
                Let Aura analyse your transaction patterns and surface smart, personalised money moves — instantly.
              </p>
            </div>
            <button @click="handleTriggerAgent" :disabled="agentLoading"
                    class="flex-shrink-0 flex items-center gap-2 bg-white text-violet-700 font-bold
                           px-5 py-2.5 rounded-xl hover:bg-violet-50 active:scale-95
                           disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200
                           shadow-sm text-sm focus:outline-none focus:ring-2 focus:ring-white/80"
                    aria-label="Trigger Aura AI to analyse your finances" :aria-busy="agentLoading">
              <span v-if="agentLoading" class="w-4 h-4 border-2 border-violet-600 border-t-transparent rounded-full animate-spin" aria-hidden="true"></span>
              <span>{{ agentLoading ? 'Analysing…' : '⚡ Analyse Now' }}</span>
            </button>
          </div>

          <Transition name="fade">
            <p v-if="agentMessage"
               class="relative mt-3.5 text-sm bg-white/15 rounded-xl px-4 py-2.5 font-medium border border-white/20"
               role="status" aria-live="polite">
              {{ agentMessage }}
            </p>
          </Transition>
        </section>

        <!-- Transactions -->
        <TransactionList :transactions="transactions" />

      </template>
    </main>

    <footer class="mt-12 border-t border-slate-200 py-6 text-center" role="contentinfo">
      <p class="text-xs text-slate-400">
        © 2025 State Bank of India &nbsp;·&nbsp; Aura AI Agent Prototype &nbsp;·&nbsp; SBI Hackathon Submission
      </p>
    </footer>

    <AuraWidget :nudges="nudges" @nudge-accepted="onNudgeAccepted" @nudge-dismissed="onNudgeDismissed" />
    <ConfettiEffect v-if="showConfetti" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AccountCard     from '../components/AccountCard.vue'
import TransactionList from '../components/TransactionList.vue'
import AuraWidget      from '../components/AuraWidget.vue'
import ConfettiEffect  from '../components/ConfettiEffect.vue'
import { getDashboard, getNudges, triggerAgent } from '../api/index.js'

const user         = ref(null)
const transactions = ref([])
const nudges       = ref([])
const loading      = ref(true)
const agentLoading = ref(false)
const agentMessage = ref('')
const showConfetti = ref(false)

let nudgeTimer = null

const firstName    = computed(() => user.value?.name?.split(' ')[0] ?? 'Rajesh')
const timeOfDay    = computed(() => { const h = new Date().getHours(); return h < 12 ? 'morning' : h < 17 ? 'afternoon' : 'evening' })
const now          = new Date()
const isoDate      = now.toISOString().slice(0, 10)
const formattedDate = now.toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })

async function loadDashboard() {
  try {
    const { data } = await getDashboard()
    user.value         = data.user
    transactions.value = data.transactions
  } catch (err) {
    console.error('[Aura] Dashboard load failed:', err)
  } finally {
    loading.value = false
  }
}

async function loadNudges() {
  try {
    const { data } = await getNudges()
    nudges.value = data.nudges
  } catch (err) {
    console.error('[Aura] Nudge load failed:', err)
  }
}

async function handleTriggerAgent() {
  agentLoading.value = true
  agentMessage.value = ''
  try {
    const { data } = await triggerAgent()
    agentMessage.value = data.message
    setTimeout(loadNudges, data.mode === 'async' ? 2500 : 800)
    setTimeout(() => { agentMessage.value = '' }, 6000)
  } catch {
    agentMessage.value = '⚠️ Could not reach the Aura agent. Please try again.'
    setTimeout(() => { agentMessage.value = '' }, 4000)
  } finally {
    agentLoading.value = false
  }
}

function onNudgeAccepted(result) {
  if (user.value) {
    user.value.checking_balance = result.new_checking_balance
    user.value.savings_balance  = result.new_savings_balance
  }
  showConfetti.value = true
  setTimeout(() => { showConfetti.value = false }, 4000)
  loadNudges()
}

function onNudgeDismissed() { loadNudges() }

onMounted(async () => {
  await Promise.all([loadDashboard(), loadNudges()])
  nudgeTimer = setInterval(loadNudges, 5000) // Poll every 5s for async Celery results
})

onUnmounted(() => { if (nudgeTimer) clearInterval(nudgeTimer) })
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>

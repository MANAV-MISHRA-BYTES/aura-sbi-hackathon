<template>
  <section class="card" aria-labelledby="txn-heading">
    <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
      <h2 id="txn-heading" class="text-base font-bold text-slate-800">Recent Transactions</h2>
      <span class="text-xs text-slate-400 bg-slate-50 px-2.5 py-1 rounded-full border border-slate-100">Last 10</span>
    </div>

    <div v-if="!transactions || transactions.length === 0"
         class="py-16 text-center text-slate-400" role="status">
      <span class="text-4xl block mb-3" aria-hidden="true">📭</span>
      <p class="font-medium">No recent transactions</p>
    </div>

    <ul v-else class="divide-y divide-slate-50/80" role="list">
      <li
        v-for="txn in transactions"
        :key="txn.id"
        class="px-6 py-4 flex items-center justify-between gap-4 hover:bg-slate-50/60 transition-colors duration-150"
        :aria-label="`${txn.type === 'credit' ? 'Credited' : 'Debited'} ₹${txn.amount.toLocaleString('en-IN')} for ${txn.category}`"
      >
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
               :class="txn.type === 'credit' ? 'bg-emerald-50' : 'bg-red-50'" aria-hidden="true">
            {{ getCategoryIcon(txn.category) }}
          </div>
          <div class="min-w-0">
            <p class="text-sm font-semibold text-slate-800 truncate">{{ txn.description }}</p>
            <p class="text-xs text-slate-400 mt-0.5">{{ txn.category }} &middot; {{ formatDate(txn.timestamp) }}</p>
          </div>
        </div>

        <div class="text-right flex-shrink-0">
          <p class="text-sm font-bold tabular-nums"
             :class="txn.type === 'credit' ? 'text-emerald-600' : 'text-red-500'">
            {{ txn.type === 'credit' ? '+' : '−' }}{{ formatCurrency(txn.amount) }}
          </p>
          <span class="text-[10px] px-2 py-0.5 rounded-full font-semibold mt-1 inline-block uppercase tracking-wide"
                :class="txn.type === 'credit' ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-500'">
            {{ txn.type }}
          </span>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({ transactions: { type: Array, default: () => [] } })

const ICONS = {
  Salary: '💼', Rent: '🏠', Groceries: '🛒', Utilities: '⚡',
  Dining: '🍽️', Transport: '🚗', Entertainment: '🎬',
  Shopping: '🛍️', Healthcare: '💊', Cashback: '🎁', Investment: '📈',
}

function getCategoryIcon(cat) { return ICONS[cat] || '💳' }

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency', currency: 'INR', maximumFractionDigits: 0,
  }).format(value)
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
  })
}
</script>

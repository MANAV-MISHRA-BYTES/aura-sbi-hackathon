<script setup>
import { onMounted } from 'vue'
import confetti from 'canvas-confetti'

const SBI_COLORS = ['#003478', '#0072BC', '#10B981', '#7C3AED', '#F59E0B', '#FFFFFF']

onMounted(() => {
  const end = Date.now() + 2_500

  // Side-burst pattern
  ;(function frame() {
    confetti({ particleCount: 4, angle: 60,  spread: 55, startVelocity: 60, origin: { x: 0, y: 0.65 }, colors: SBI_COLORS })
    confetti({ particleCount: 4, angle: 120, spread: 55, startVelocity: 60, origin: { x: 1, y: 0.65 }, colors: SBI_COLORS })
    if (Date.now() < end) requestAnimationFrame(frame)
  })()
})
</script>

<template>
  <div aria-hidden="true"></div>
</template>

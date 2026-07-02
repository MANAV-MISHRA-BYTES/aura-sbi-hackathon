import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 12_000,
  headers: { 'Content-Type': 'application/json' },
})

export const getDashboard = ()           => api.get('/dashboard')
export const getNudges    = ()           => api.get('/nudges')
export const executeNudge = (nudge_id)   => api.post('/execute-nudge', { nudge_id })
export const dismissNudge = (nudge_id)   => api.post('/dismiss-nudge', { nudge_id })
export const triggerAgent = ()           => api.post('/trigger-agent')

export default api

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface RiskScore {
  id: number
  region_id: string
  timestamp: string
  risk_probability: number
  risk_level: string
  contributing_factors?: string
}

export interface Alert {
  id: number
  region_id: string
  alert_type: string
  severity: string
  title: string
  message: string
  is_read: boolean
  is_acknowledged: boolean
  created_at: string
}

export interface GetRiskScoresParams {
  region_id?: string
  start_date?: string
  end_date?: string
  tenant_id?: number
  limit?: number
}

export interface GetAlertsParams {
  region_id?: string
  alert_type?: string
  severity?: string
  is_read?: boolean
  tenant_id?: number
  limit?: number
}

export const getLatestRiskScores = async (tenant_id?: number) => {
  const response = await api.get('/risk/scores/latest', {
    params: { tenant_id },
  })
  return response.data
}

export const getRiskScores = async (params: GetRiskScoresParams) => {
  const response = await api.get('/risk/scores', { params })
  return response.data
}

export const getAlerts = async (params: GetAlertsParams = {}) => {
  const response = await api.get('/alerts', { params })
  return response.data
}

export const markAlertRead = async (alertId: number) => {
  const response = await api.patch(`/alerts/${alertId}/read`)
  return response.data
}

export const acknowledgeAlert = async (alertId: number) => {
  const response = await api.patch(`/alerts/${alertId}/acknowledge`)
  return response.data
}

export const queryLLM = async (query: string, context?: Record<string, any>) => {
  const response = await api.post('/llm/query', {
    query,
    context,
  })
  return response.data
}

export default api


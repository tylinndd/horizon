import axios from 'axios'

// Use relative path when served from same domain, or environment variable for separate deployment
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

// Hospital API endpoints
export interface HospitalDashboard {
  facility_id: string
  facility_name: string
  region_id: string
  budget: {
    id: number
    total_budget: number
    allocated_budget: number
    available_budget: number
    risk_adjusted_budget: number | null
    recommended_allocation: any
    timestamp: string
  } | null
  risk_score: {
    risk_level: string
    risk_probability: number
    contributing_factors: string
    timestamp: string
  } | null
  resource_allocations: Array<{
    id: number
    resource_type: string
    current_capacity: number
    recommended_capacity: number
    utilization_rate: number
    priority_level: string
    allocation_reason: string | null
  }>
  recommendations: Array<{
    id: number
    title: string
    description: string
    priority: string
    recommendation_type: string
    estimated_impact: string | null
    estimated_cost: number | null
    estimated_savings: number | null
    timeframe: string | null
  }>
}

export const getHospitalDashboard = async (facilityId: string, tenantId?: number) => {
  const response = await api.get('/hospital/dashboard', {
    params: { facility_id: facilityId, tenant_id: tenantId },
  })
  return response.data as HospitalDashboard
}

export default api


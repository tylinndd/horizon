import { useEffect, useState } from 'react'
import { getLatestRiskScores, getAlerts } from '../services/api'
import RiskScoreCard from '../components/RiskScoreCard'
import AlertCard from '../components/AlertCard'
import TrendChart from '../components/TrendChart'
import HorizonAssistant from '../components/HorizonAssistant'
import './Dashboard.css'

interface RiskScore {
  id: number
  region_id: string
  risk_probability: number
  risk_level: string
  contributing_factors?: string
}

interface Alert {
  id: number
  region_id: string
  alert_type: string
  severity: string
  title: string
  message: string
  is_read: boolean
  created_at: string
}

export default function Dashboard() {
  const [riskScores, setRiskScores] = useState<RiskScore[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
    // Refresh every 5 minutes
    const interval = setInterval(loadData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      const [riskData, alertsData] = await Promise.all([
        getLatestRiskScores(),
        getAlerts({ limit: 5, is_read: false })
      ])
      setRiskScores(riskData.scores || [])
      setAlerts(alertsData.alerts || [])
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  const criticalRegions = riskScores.filter(
    (r) => r.risk_level === 'critical' || r.risk_level === 'high'
  )

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Dashboard</h1>

      <div className="dashboard-grid">
        <div className="dashboard-section">
          <h2 className="section-title">Risk Overview</h2>
          <div className="risk-cards">
            {criticalRegions.length > 0 ? (
              criticalRegions.map((score) => (
                <RiskScoreCard key={score.id} score={score} />
              ))
            ) : (
              <div className="empty-state">No high-risk regions detected</div>
            )}
          </div>
        </div>

        <div className="dashboard-section">
          <h2 className="section-title">Recent Alerts</h2>
          <div className="alerts-list">
            {alerts.length > 0 ? (
              alerts.map((alert) => (
                <AlertCard key={alert.id} alert={alert} />
              ))
            ) : (
              <div className="empty-state">No active alerts</div>
            )}
          </div>
        </div>

        <div className="dashboard-section full-width">
          <h2 className="section-title">Risk Trends</h2>
          <TrendChart />
        </div>

        <div className="dashboard-section full-width">
          <h2 className="section-title">Horizon Assistant</h2>
          <HorizonAssistant />
        </div>
      </div>
    </div>
  )
}


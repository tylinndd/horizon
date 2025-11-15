import { useEffect, useState } from 'react'
import { getAlerts, markAlertRead, acknowledgeAlert } from '../services/api'
import AlertCard from '../components/AlertCard'
import './Alerts.css'

interface Alert {
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

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'unread' | 'critical'>('all')

  useEffect(() => {
    loadAlerts()
  }, [filter])

  const loadAlerts = async () => {
    try {
      const params: any = { limit: 100 }
      if (filter === 'unread') {
        params.is_read = false
      }
      if (filter === 'critical') {
        params.severity = 'critical'
      }
      const response = await getAlerts(params)
      setAlerts(response.alerts || [])
    } catch (error) {
      console.error('Error loading alerts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleMarkRead = async (alertId: number) => {
    try {
      await markAlertRead(alertId)
      loadAlerts()
    } catch (error) {
      console.error('Error marking alert as read:', error)
    }
  }

  const handleAcknowledge = async (alertId: number) => {
    try {
      await acknowledgeAlert(alertId)
      loadAlerts()
    } catch (error) {
      console.error('Error acknowledging alert:', error)
    }
  }

  if (loading) {
    return <div className="loading">Loading alerts...</div>
  }

  return (
    <div className="alerts-page">
      <div className="alerts-header">
        <h1 className="page-title">Alerts</h1>
        <div className="alerts-filters">
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
            onClick={() => setFilter('unread')}
          >
            Unread
          </button>
          <button
            className={`filter-btn ${filter === 'critical' ? 'active' : ''}`}
            onClick={() => setFilter('critical')}
          >
            Critical
          </button>
        </div>
      </div>

      <div className="alerts-container">
        {alerts.length > 0 ? (
          alerts.map((alert) => (
            <div key={alert.id} className="alert-wrapper">
              <AlertCard alert={alert} />
              <div className="alert-actions">
                {!alert.is_read && (
                  <button
                    className="action-btn"
                    onClick={() => handleMarkRead(alert.id)}
                  >
                    Mark as Read
                  </button>
                )}
                {!alert.is_acknowledged && (
                  <button
                    className="action-btn action-btn-primary"
                    onClick={() => handleAcknowledge(alert.id)}
                  >
                    Acknowledge
                  </button>
                )}
              </div>
            </div>
          ))
        ) : (
          <div className="empty-state">No alerts found</div>
        )}
      </div>
    </div>
  )
}


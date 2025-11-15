import { Alert } from '../pages/Dashboard'
import './AlertCard.css'

interface AlertCardProps {
  alert: Alert
}

export default function AlertCard({ alert }: AlertCardProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'var(--color-red)'
      case 'high':
        return 'var(--color-red-light)'
      case 'medium':
        return '#facc15'
      default:
        return 'var(--color-gray)'
    }
  }

  return (
    <div className="alert-card" style={{ borderLeftColor: getSeverityColor(alert.severity) }}>
      <div className="alert-header">
        <div>
          <h4 className="alert-title">{alert.title}</h4>
          <span className="alert-region">{alert.region_id}</span>
        </div>
        <span className={`alert-severity severity-${alert.severity}`}>
          {alert.severity.toUpperCase()}
        </span>
      </div>
      <p className="alert-message">{alert.message}</p>
      <div className="alert-footer">
        <span className="alert-time">
          {new Date(alert.created_at).toLocaleString()}
        </span>
        {!alert.is_read && <span className="alert-unread">NEW</span>}
      </div>
    </div>
  )
}


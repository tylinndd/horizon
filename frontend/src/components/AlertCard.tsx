import './AlertCard.css'

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

interface AlertCardProps {
  alert: Alert
  onClick?: () => void
}

export default function AlertCard({ alert, onClick }: AlertCardProps) {
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
    <div 
      className="alert-card" 
      style={{ borderLeftColor: getSeverityColor(alert.severity), cursor: onClick ? 'pointer' : 'default' }}
      onClick={onClick}
    >
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


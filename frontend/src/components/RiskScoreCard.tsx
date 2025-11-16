import './RiskScoreCard.css'

interface RiskScore {
  id: number
  region_id: string
  risk_probability: number
  risk_level: string
  contributing_factors?: string
}

interface RiskScoreCardProps {
  score: RiskScore
  onClick?: () => void
}

export default function RiskScoreCard({ score, onClick }: RiskScoreCardProps) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'critical':
        return 'var(--color-red)'
      case 'high':
        return 'var(--color-orange)' // Orange - more distinct
      case 'medium':
        return '#facc15' // Lighter yellow
      default:
        return 'var(--color-gray)'
    }
  }

  return (
    <div 
      className="risk-score-card" 
      style={{ borderLeftColor: getRiskColor(score.risk_level), cursor: onClick ? 'pointer' : 'default' }}
      onClick={onClick}
    >
      <div className="risk-score-header">
        <h3 className="risk-region">{score.region_id}</h3>
        <span className={`risk-badge risk-${score.risk_level}`}>
          {score.risk_level.toUpperCase()}
        </span>
      </div>
      <div className="risk-probability">
        {(score.risk_probability * 100).toFixed(1)}%
      </div>
      {score.contributing_factors && (
        <div className="risk-factors">
          {score.contributing_factors}
        </div>
      )}
    </div>
  )
}


import { RiskScore } from '../pages/Dashboard'
import './RiskScoreCard.css'

interface RiskScoreCardProps {
  score: RiskScore
}

export default function RiskScoreCard({ score }: RiskScoreCardProps) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'critical':
        return 'var(--color-red)'
      case 'high':
        return 'var(--color-red-light)'
      case 'medium':
        return '#f59e0b'
      default:
        return 'var(--color-gray)'
    }
  }

  return (
    <div className="risk-score-card" style={{ borderLeftColor: getRiskColor(score.risk_level) }}>
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


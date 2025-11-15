import { useEffect, useState } from 'react'
import { getLatestRiskScores } from '../services/api'
import './RiskMap.css'

interface RiskScore {
  id: number
  region_id: string
  risk_probability: number
  risk_level: string
}

export default function RiskMap() {
  const [riskScores, setRiskScores] = useState<RiskScore[]>([])
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadRiskScores()
  }, [])

  const loadRiskScores = async () => {
    try {
      const response = await getLatestRiskScores()
      setRiskScores(response.scores || [])
    } catch (error) {
      console.error('Error loading risk scores:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'critical':
        return '#dc2626'
      case 'high':
        return '#ef4444'
      case 'medium':
        return '#f59e0b'
      case 'low':
        return '#737373'
      default:
        return '#e5e5e5'
    }
  }

  if (loading) {
    return <div className="loading">Loading risk map...</div>
  }

  const selectedScore = selectedRegion
    ? riskScores.find((s) => s.region_id === selectedRegion)
    : null

  return (
    <div className="risk-map-page">
      <h1 className="page-title">Risk Map</h1>

      <div className="risk-map-container">
        <div className="map-placeholder">
          <div className="map-grid">
            {riskScores.map((score) => (
              <div
                key={score.id}
                className="map-region"
                style={{
                  backgroundColor: getRiskColor(score.risk_level),
                  opacity: selectedRegion && selectedRegion !== score.region_id ? 0.3 : 1
                }}
                onClick={() => setSelectedRegion(score.region_id)}
              >
                <div className="region-label">{score.region_id}</div>
                <div className="region-risk">{(score.risk_probability * 100).toFixed(0)}%</div>
              </div>
            ))}
          </div>
          <div className="map-legend">
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#dc2626' }}></div>
              <span>Critical</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
              <span>High</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#f59e0b' }}></div>
              <span>Medium</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#737373' }}></div>
              <span>Low</span>
            </div>
          </div>
        </div>

        {selectedScore && (
          <div className="region-details">
            <h2 className="details-title">{selectedScore.region_id}</h2>
            <div className="details-content">
              <div className="detail-item">
                <span className="detail-label">Risk Level:</span>
                <span className={`detail-value risk-${selectedScore.risk_level}`}>
                  {selectedScore.risk_level.toUpperCase()}
                </span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Risk Probability:</span>
                <span className="detail-value">
                  {(selectedScore.risk_probability * 100).toFixed(1)}%
                </span>
              </div>
            </div>
            <button
              className="close-details"
              onClick={() => setSelectedRegion(null)}
            >
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  )
}


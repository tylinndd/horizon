import { useEffect, useState, useRef } from 'react'
import { getLatestRiskScores } from '../services/api'
import Globe from 'react-globe.gl'
import HorizonAssistant from '../components/HorizonAssistant'
import './Homepage.css'

interface RiskScore {
  id: number
  region_id: string
  risk_probability: number
  risk_level: string
  contributing_factors?: string
}

interface OutbreakInfo {
  region: string
  type: string
  description: string
  riskLevel: string
}

// US State coordinates (lat, lng)
const stateCoordinates: { [key: string]: [number, number] } = {
  'US-CA': [36.7783, -119.4179], // California
  'US-NY': [40.7128, -74.0060],  // New York
  'US-TX': [31.9686, -99.9018],  // Texas
  'US-FL': [27.7663, -81.6868],  // Florida
  'US-IL': [40.3495, -88.9861],  // Illinois
}

// Mock outbreak types based on region
const getOutbreakInfo = (region: string, riskLevel: string): OutbreakInfo => {
  const outbreaks: { [key: string]: string[] } = {
    'US-CA': ['Influenza-like illness', 'Respiratory syncytial virus', 'COVID-19 variant'],
    'US-NY': ['Seasonal flu', 'Norovirus', 'Respiratory infections'],
    'US-TX': ['Dengue fever', 'West Nile virus', 'Respiratory illness'],
    'US-FL': ['Dengue fever', 'Zika virus', 'Respiratory syncytial virus'],
    'US-IL': ['Influenza', 'Respiratory infections', 'Gastrointestinal illness']
  }
  
  const types = outbreaks[region] || ['Respiratory illness', 'Seasonal flu', 'General outbreak']
  const randomType = types[Math.floor(Math.random() * types.length)]
  
  return {
    region,
    type: randomType,
    description: `Elevated cases of ${randomType.toLowerCase()} detected in ${region}. Increased hospital visits and pharmacy purchases indicate potential outbreak.`,
    riskLevel
  }
}

export default function Homepage() {
  const [riskScores, setRiskScores] = useState<RiskScore[]>([])
  const [selectedOutbreak, setSelectedOutbreak] = useState<OutbreakInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const globeEl = useRef<any>()

  useEffect(() => {
    loadRiskScores()
  }, [])

  useEffect(() => {
    if (globeEl.current && riskScores.length > 0) {
      // Auto-rotate the globe
      globeEl.current.controls().autoRotate = true
      globeEl.current.controls().autoRotateSpeed = 0.5
    }
  }, [riskScores])

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
        return '#f97316' // Orange
      case 'medium':
        return '#facc15' // Lighter yellow
      case 'low':
        return '#737373'
      default:
        return '#e5e5e5'
    }
  }

  // Convert risk scores to points for the globe
  const points = riskScores.map(score => {
    const coords = stateCoordinates[score.region_id] || [0, 0]
    return {
      lat: coords[0],
      lng: coords[1],
      size: score.risk_probability * 0.5 + 0.3,
      color: getRiskColor(score.risk_level),
      region: score.region_id,
      riskLevel: score.risk_level,
      riskProbability: score.risk_probability,
      score: score
    }
  })

  const handlePointClick = (point: any) => {
    const score = point.score as RiskScore
    const outbreakInfo = getOutbreakInfo(score.region_id, score.risk_level)
    setSelectedOutbreak(outbreakInfo)
    
    // Focus on the clicked point
    if (globeEl.current) {
      globeEl.current.pointOfView({
        lat: point.lat,
        lng: point.lng,
        altitude: 2
      }, 1000)
    }
  }

  if (loading) {
    return <div className="homepage-loading">Loading outbreak map...</div>
  }

  return (
    <div className="homepage">
      <div className="homepage-header">
        <h1 className="homepage-title">Global Outbreak Detection</h1>
        <p className="homepage-subtitle">Real-time monitoring of health risks worldwide</p>
      </div>

      <div className="homepage-content">
        <div className="globe-container">
          <div className="globe-wrapper">
            <Globe
              ref={globeEl}
              globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
              backgroundImageUrl="//unpkg.com/three-globe/example/img/night-sky.png"
              pointsData={points}
              pointColor="color"
              pointRadius="size"
              pointLabel={(point: any) => `
                <div style="
                  background: white;
                  padding: 8px;
                  border-radius: 4px;
                  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                  font-size: 12px;
                ">
                  <strong>${point.region}</strong><br/>
                  Risk: ${(point.riskProbability * 100).toFixed(0)}%<br/>
                  Level: ${point.riskLevel.toUpperCase()}
                </div>
              `}
              onPointClick={handlePointClick}
              pointResolution={2}
              enablePointerInteraction={true}
            />
            <div className="globe-controls">
              <button 
                className="globe-btn"
                onClick={() => {
                  if (globeEl.current) {
                    globeEl.current.controls().autoRotate = !globeEl.current.controls().autoRotate
                  }
                }}
              >
                Toggle Rotation
              </button>
              <button 
                className="globe-btn"
                onClick={() => {
                  if (globeEl.current) {
                    globeEl.current.pointOfView({ lat: 0, lng: 0, altitude: 2.5 }, 1000)
                  }
                }}
              >
                Reset View
              </button>
            </div>
            <div className="globe-legend">
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: '#dc2626' }}></div>
                <span>Critical</span>
              </div>
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: '#f97316' }}></div>
                <span>High</span>
              </div>
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: '#facc15' }}></div>
                <span>Medium</span>
              </div>
              <div className="legend-item">
                <div className="legend-color" style={{ backgroundColor: '#737373' }}></div>
                <span>Low</span>
              </div>
            </div>
          </div>

          {selectedOutbreak && (
            <div className="outbreak-details">
              <button className="close-outbreak" onClick={() => setSelectedOutbreak(null)}>×</button>
              <h2 className="outbreak-region">{selectedOutbreak.region}</h2>
              <div className="outbreak-type">
                <span className="type-label">Outbreak Type:</span>
                <span className="type-value">{selectedOutbreak.type}</span>
              </div>
              <div className="outbreak-risk">
                <span className="risk-label">Risk Level:</span>
                <span className={`risk-badge risk-${selectedOutbreak.riskLevel}`}>
                  {selectedOutbreak.riskLevel.toUpperCase()}
                </span>
              </div>
              <p className="outbreak-description">{selectedOutbreak.description}</p>
            </div>
          )}
        </div>

        <div className="assistant-section">
          <h2 className="section-title">Horizon Assistant</h2>
          <HorizonAssistant />
        </div>
      </div>
    </div>
  )
}

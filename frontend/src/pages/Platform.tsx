import { useEffect, useState, useRef } from 'react'
import { getLatestRiskScores } from '../services/api'
import Globe from 'react-globe.gl'
import HorizonAssistant from '../components/HorizonAssistant'
import './Platform.css'

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

export default function Platform() {
  const [riskScores, setRiskScores] = useState<RiskScore[]>([])
  const [selectedOutbreak, setSelectedOutbreak] = useState<OutbreakInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [showAssistant, setShowAssistant] = useState(false)
  const globeEl = useRef<any>()

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  useEffect(() => {
    loadRiskScores()
  }, [])

  useEffect(() => {
    if (globeEl.current && riskScores.length > 0) {
      // Center on United States
      globeEl.current.pointOfView({
        lat: 37.0902,
        lng: -95.7129,
        altitude: 1.5
      }, 0)
      
      // Disable auto-rotate for better control
      globeEl.current.controls().autoRotate = false
      globeEl.current.controls().enableZoom = true
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
        return '#f97316'
      case 'medium':
        return '#facc15'
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
      size: score.risk_probability * 0.8 + 0.4,
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
        altitude: 1.2
      }, 1000)
    }
  }

  if (loading) {
    return (
      <div className="platform-loading">
        <div className="loading-spinner"></div>
        <p>Initializing outbreak detection system...</p>
      </div>
    )
  }

  return (
    <div className="platform-page">
      <div className="globe-container-fullscreen">
        <Globe
          ref={globeEl}
          globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
          backgroundImageUrl="//unpkg.com/three-globe/example/img/night-sky.png"
          pointsData={points}
          pointColor="color"
          pointRadius="size"
          pointAltitude={0.01}
          pointLabel={(point: any) => `
            <div style="
              background: rgba(0, 0, 0, 0.9);
              padding: 12px;
              border-radius: 8px;
              box-shadow: 0 4px 16px rgba(0,0,0,0.5);
              font-size: 13px;
              color: white;
              border: 1px solid ${point.color};
            ">
              <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">${point.region}</div>
              <div>Risk: <span style="color: ${point.color}; font-weight: 600;">${(point.riskProbability * 100).toFixed(0)}%</span></div>
              <div>Level: <span style="color: ${point.color}; font-weight: 600;">${point.riskLevel.toUpperCase()}</span></div>
            </div>
          `}
          onPointClick={handlePointClick}
          pointResolution={4}
          enablePointerInteraction={true}
          width={window.innerWidth}
          height={window.innerHeight}
        />

        {selectedOutbreak && (
          <div className="outbreak-panel">
            <button className="close-panel" onClick={() => setSelectedOutbreak(null)}>×</button>
            <div className="panel-header">
              <h2>{selectedOutbreak.region}</h2>
              <span className={`risk-badge-large risk-${selectedOutbreak.riskLevel}`}>
                {selectedOutbreak.riskLevel.toUpperCase()}
              </span>
            </div>
            <div className="panel-content">
              <div className="outbreak-detail">
                <div className="detail-label">Outbreak Type</div>
                <div className="detail-value">{selectedOutbreak.type}</div>
              </div>
              <div className="outbreak-description">{selectedOutbreak.description}</div>
            </div>
          </div>
        )}

        {/* AI Assistant Floating Button */}
        <button 
          className="assistant-toggle"
          onClick={() => setShowAssistant(!showAssistant)}
          title="AI Assistant"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 18a8 8 0 110-16 8 8 0 010 16z" fill="currentColor"/>
            <path d="M12 6v6l4 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>

        {/* AI Assistant Popup */}
        {showAssistant && (
          <div className="assistant-popup">
            <div className="assistant-popup-header">
              <h3>AI Assistant</h3>
              <button onClick={() => setShowAssistant(false)} className="close-popup">×</button>
            </div>
            <div className="assistant-popup-content">
              <HorizonAssistant />
            </div>
          </div>
        )}

        {/* Risk Level Legend */}
        <div className="globe-legend">
          <div className="legend-title">Risk Level</div>
          <div className="legend-items">
            <div className="legend-item">
              <div className="legend-dot" style={{ backgroundColor: '#dc2626' }}></div>
              <span>Critical</span>
            </div>
            <div className="legend-item">
              <div className="legend-dot" style={{ backgroundColor: '#f97316' }}></div>
              <span>High</span>
            </div>
            <div className="legend-item">
              <div className="legend-dot" style={{ backgroundColor: '#facc15' }}></div>
              <span>Medium</span>
            </div>
            <div className="legend-item">
              <div className="legend-dot" style={{ backgroundColor: '#737373' }}></div>
              <span>Low</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


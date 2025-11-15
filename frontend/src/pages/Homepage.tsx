import { useNavigate } from 'react-router-dom'
import { useEffect, useState, useRef } from 'react'
import './Homepage.css'

export default function Homepage() {
  const navigate = useNavigate()
  const [scrollProgress, setScrollProgress] = useState(0)
  const [currentVideo, setCurrentVideo] = useState(1)
  const videoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollHeight - window.innerHeight
      const currentScroll = window.scrollY
      setScrollProgress((currentScroll / totalScroll) * 100)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleVideoEnd = () => {
    // Switch to the next video
    setCurrentVideo(prev => prev === 1 ? 2 : 1)
  }

  useEffect(() => {
    // Reload and play video when source changes
    if (videoRef.current) {
      videoRef.current.load()
      videoRef.current.play().catch(err => console.log('Video play error:', err))
    }
  }, [currentVideo])

  return (
    <div className="landing-page">
      <div className="scroll-indicator" style={{ width: `${scrollProgress}%` }} />
      
      {/* Hero Section */}
      <section className="hero-section">
        <div className="video-background">
          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            className="hero-video"
            onEnded={handleVideoEnd}
          >
            <source 
              src={currentVideo === 1 ? "/horizon-vid1.mp4" : "/horizon-vid2.mp4"} 
              type="video/mp4" 
            />
          </video>
          <div className="video-overlay"></div>
        </div>
        <div className="hero-content">
          <h1 className="hero-title">
            Early detection saves lives
          </h1>
          <p className="hero-description">
            Identify outbreak patterns days before traditional surveillance systems
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          <div className="stat-block">
            <div className="stat-value">2-3 days</div>
            <div className="stat-description">earlier warning than traditional methods</div>
          </div>
          <div className="stat-block">
            <div className="stat-value">99.2%</div>
            <div className="stat-description">detection accuracy across signals</div>
          </div>
          <div className="stat-block">
            <div className="stat-value">Real-time</div>
            <div className="stat-description">continuous monitoring and analysis</div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="problem-section">
        <div className="section-content-wide">
          <h2 className="section-heading">
            By the time official reports confirm an outbreak,<br />
            it's already too late
          </h2>
          <div className="problem-details">
            <div className="detail-column">
              <h3>The cost of delay</h3>
              <p>
                Traditional surveillance systems rely on manual reporting, lab confirmations, 
                and bureaucratic channels. The average 7-14 day detection lag allows outbreaks 
                to spread exponentially.
              </p>
            </div>
            <div className="detail-column">
              <h3>Missing the early signals</h3>
              <p>
                Critical indicators exist in pharmacy sales, search patterns, and hospital 
                utilization long before official case reports. These signals remain invisible 
                to conventional systems.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="solution-section">
        <div className="section-content-narrow">
          <h2 className="large-heading">
            We detect the invisible
          </h2>
          <p className="solution-text">
            Horizon analyzes dozens of real-time data sources—from search trends to pharmacy 
            purchases—to identify anomalies that signal emerging outbreaks. Our models flag 
            threats before they appear in official statistics.
          </p>
        </div>
      </section>

      {/* Capabilities Section */}
      <section className="capabilities-section">
        <div className="section-content-wide">
          <div className="capability-item">
            <div className="capability-number">01</div>
            <div className="capability-content">
              <h3>Multi-signal detection</h3>
              <p>
                Synthesize data from public health APIs, pharmacy aggregates, search trends, 
                hospital systems, and syndromic surveillance. Pattern recognition across 
                diverse sources reveals threats others miss.
              </p>
            </div>
          </div>

          <div className="capability-item">
            <div className="capability-number">02</div>
            <div className="capability-content">
              <h3>Anomaly identification</h3>
              <p>
                Machine learning models trained on historical outbreak data identify unusual 
                patterns in real-time. Statistical outliers trigger immediate investigation 
                before human analysts see the trends.
              </p>
            </div>
          </div>

          <div className="capability-item">
            <div className="capability-number">03</div>
            <div className="capability-content">
              <h3>Risk quantification</h3>
              <p>
                Every region receives a continuously updated risk score. Probability-based 
                assessments enable proactive resource allocation and targeted interventions 
                in high-risk areas.
              </p>
            </div>
          </div>

          <div className="capability-item">
            <div className="capability-number">04</div>
            <div className="capability-content">
              <h3>Intelligent response</h3>
              <p>
                Natural language interface provides instant answers to complex questions. 
                Decision-makers query risk factors, explore scenarios, and access insights 
                without waiting for analyst reports.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="impact-section">
        <div className="section-content-narrow">
          <h2 className="medium-heading">
            Built for organizations that can't afford to wait
          </h2>
          <div className="impact-grid">
            <div className="impact-item">
              <h4>Public health</h4>
              <p>State and local agencies gain early warning systems that enable proactive containment</p>
            </div>
            <div className="impact-item">
              <h4>Healthcare systems</h4>
              <p>Hospitals optimize capacity planning and resource allocation ahead of demand surges</p>
            </div>
            <div className="impact-item">
              <h4>Insurance</h4>
              <p>Risk models incorporate real-time outbreak data for dynamic pricing and exposure management</p>
            </div>
            <div className="impact-item">
              <h4>Research</h4>
              <p>Academic institutions access rich datasets for epidemiological modeling and outbreak analysis</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="final-cta">
        <div className="cta-content">
          <h2 className="cta-heading">
            See it in action
          </h2>
          <button 
            className="primary-button"
            onClick={() => navigate('/platform')}
          >
            Launch platform
          </button>
        </div>
      </section>
    </div>
  )
}

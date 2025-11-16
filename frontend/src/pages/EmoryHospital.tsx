import { useEffect, useState } from 'react'
import { getHospitalDashboard, HospitalDashboard } from '../services/api'
import './EmoryHospital.css'

export default function EmoryHospital() {
  const [dashboard, setDashboard] = useState<HospitalDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    window.scrollTo(0, 0)
    loadDashboard()
    // Refresh every 5 minutes
    const interval = setInterval(loadDashboard, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const loadDashboard = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getHospitalDashboard('emory-main', 1)
      setDashboard(data)
    } catch (err: any) {
      console.error('Error loading dashboard:', err)
      setError(err.message || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount * 1000000) // Convert millions to actual amount
  }

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`
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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
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

  if (loading) {
    return (
      <div className="emory-loading">
        <div className="loading-spinner"></div>
        <p>Loading Emory Hospital dashboard...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="emory-error">
        <h2>Error Loading Dashboard</h2>
        <p>{error}</p>
        <button onClick={loadDashboard}>Retry</button>
      </div>
    )
  }

  if (!dashboard) {
    return (
      <div className="emory-error">
        <h2>No Data Available</h2>
        <p>No dashboard data found for Emory Hospital.</p>
      </div>
    )
  }

  return (
    <div className="emory-hospital-page">
      <div className="emory-header">
        <div className="emory-header-content">
          <h1>{dashboard.facility_name}</h1>
          <p className="emory-subtitle">Integrated Health Intelligence Dashboard</p>
          {dashboard.risk_score && (
            <div className="emory-risk-badge" style={{ backgroundColor: getRiskColor(dashboard.risk_score.risk_level) }}>
              <span className="risk-label">Regional Risk Level:</span>
              <span className="risk-value">{dashboard.risk_score.risk_level.toUpperCase()}</span>
              <span className="risk-probability">({formatPercentage(dashboard.risk_score.risk_probability)})</span>
            </div>
          )}
        </div>
      </div>

      <div className="emory-content">
        {/* Budget Section */}
        {dashboard.budget && (
          <section className="emory-section">
            <h2>Budget Overview</h2>
            <div className="budget-grid">
              <div className="budget-card">
                <div className="budget-label">Total Budget</div>
                <div className="budget-value">{formatCurrency(dashboard.budget.total_budget)}</div>
                <div className="budget-period">Quarterly Allocation</div>
              </div>
              <div className="budget-card">
                <div className="budget-label">Allocated</div>
                <div className="budget-value">{formatCurrency(dashboard.budget.allocated_budget)}</div>
                <div className="budget-percentage">
                  {formatPercentage(dashboard.budget.allocated_budget / dashboard.budget.total_budget)}
                </div>
              </div>
              <div className="budget-card">
                <div className="budget-label">Available</div>
                <div className="budget-value">{formatCurrency(dashboard.budget.available_budget)}</div>
                <div className="budget-percentage">
                  {formatPercentage(dashboard.budget.available_budget / dashboard.budget.total_budget)}
                </div>
              </div>
              {dashboard.budget.risk_adjusted_budget && (
                <div className="budget-card risk-adjusted">
                  <div className="budget-label">Risk-Adjusted Budget</div>
                  <div className="budget-value">{formatCurrency(dashboard.budget.risk_adjusted_budget)}</div>
                  <div className="budget-note">Based on current risk level</div>
                </div>
              )}
            </div>

            {dashboard.budget.recommended_allocation && (
              <div className="recommendations-box">
                <h3>Recommended Budget Adjustments</h3>
                <div className="recommendations-list">
                  {Object.entries(dashboard.budget.recommended_allocation).map(([category, rec]: [string, any]) => (
                    <div key={category} className="recommendation-item">
                      <div className="rec-category">{category.replace('_', ' ').toUpperCase()}</div>
                      <div className="rec-details">
                        <div className="rec-current">
                          Current: {formatCurrency(rec.current)}
                        </div>
                        <div className="rec-arrow">→</div>
                        <div className="rec-recommended">
                          Recommended: {formatCurrency(rec.recommended)}
                        </div>
                      </div>
                      <div className="rec-reason">{rec.reason}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {/* Resource Allocations */}
        {dashboard.resource_allocations.length > 0 && (
          <section className="emory-section">
            <h2>Resource Allocation Recommendations</h2>
            <div className="resources-grid">
              {dashboard.resource_allocations.map((resource) => (
                <div key={resource.id} className="resource-card">
                  <div className="resource-header">
                    <h3>{resource.resource_type.toUpperCase()}</h3>
                    <span
                      className="priority-badge"
                      style={{ backgroundColor: getPriorityColor(resource.priority_level) }}
                    >
                      {resource.priority_level}
                    </span>
                  </div>
                  <div className="resource-metrics">
                    <div className="metric">
                      <div className="metric-label">Current Capacity</div>
                      <div className="metric-value">{resource.current_capacity.toLocaleString()}</div>
                    </div>
                    <div className="metric">
                      <div className="metric-label">Recommended Capacity</div>
                      <div className="metric-value recommended">
                        {resource.recommended_capacity.toLocaleString()}
                      </div>
                    </div>
                    <div className="metric">
                      <div className="metric-label">Utilization Rate</div>
                      <div className="metric-value">{formatPercentage(resource.utilization_rate)}</div>
                      <div className="utilization-bar">
                        <div
                          className="utilization-fill"
                          style={{
                            width: formatPercentage(resource.utilization_rate),
                            backgroundColor: resource.utilization_rate > 0.8 ? '#dc2626' : resource.utilization_rate > 0.6 ? '#f97316' : '#10b981'
                          }}
                        />
                      </div>
                    </div>
                  </div>
                  {resource.allocation_reason && (
                    <div className="resource-reason">{resource.allocation_reason}</div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Recommendations */}
        {dashboard.recommendations.length > 0 && (
          <section className="emory-section">
            <h2>AI-Powered Recommendations</h2>
            <div className="recommendations-grid">
              {dashboard.recommendations.map((rec) => (
                <div key={rec.id} className="recommendation-card">
                  <div className="rec-header">
                    <h3>{rec.title}</h3>
                    <div className="rec-badges">
                      <span
                        className="priority-badge"
                        style={{ backgroundColor: getPriorityColor(rec.priority) }}
                      >
                        {rec.priority}
                      </span>
                      <span className="type-badge">{rec.recommendation_type}</span>
                    </div>
                  </div>
                  <p className="rec-description">{rec.description}</p>
                  {rec.estimated_impact && (
                    <div className="rec-impact">
                      <strong>Impact:</strong> {rec.estimated_impact}
                    </div>
                  )}
                  <div className="rec-financials">
                    {rec.estimated_cost && (
                      <div className="rec-cost">
                        <strong>Cost:</strong> {formatCurrency(rec.estimated_cost)}
                      </div>
                    )}
                    {rec.estimated_savings && (
                      <div className="rec-savings">
                        <strong>Annual Savings:</strong> {formatCurrency(rec.estimated_savings)}
                      </div>
                    )}
                  </div>
                  {rec.timeframe && (
                    <div className="rec-timeframe">
                      <strong>Timeframe:</strong> {rec.timeframe}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Risk Score Details */}
        {dashboard.risk_score && (
          <section className="emory-section">
            <h2>Regional Risk Assessment</h2>
            <div className="risk-details">
              <div className="risk-info">
                <div className="risk-metric">
                  <div className="risk-label">Risk Level</div>
                  <div
                    className="risk-value-large"
                    style={{ color: getRiskColor(dashboard.risk_score.risk_level) }}
                  >
                    {dashboard.risk_score.risk_level.toUpperCase()}
                  </div>
                </div>
                <div className="risk-metric">
                  <div className="risk-label">Risk Probability</div>
                  <div className="risk-value-large">
                    {formatPercentage(dashboard.risk_score.risk_probability)}
                  </div>
                </div>
              </div>
              {dashboard.risk_score.contributing_factors && (
                <div className="risk-factors">
                  <h3>Contributing Factors</h3>
                  <p>{dashboard.risk_score.contributing_factors}</p>
                </div>
              )}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}


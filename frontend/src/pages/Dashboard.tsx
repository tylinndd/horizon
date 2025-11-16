import { useEffect, useState } from 'react'
import { getLatestRiskScores, getAlerts, getHospitalDashboard, HospitalDashboard } from '../services/api'
import RiskScoreCard from '../components/RiskScoreCard'
import AlertCard from '../components/AlertCard'
import TrendChart from '../components/TrendChart'
import HorizonAssistant from '../components/HorizonAssistant'
import CardModal from '../components/CardModal'
import './Dashboard.css'

interface RiskScore {
  id: number
  region_id: string
  risk_probability: number
  risk_level: string
  contributing_factors?: string
}

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

export default function Dashboard() {
  const [riskScores, setRiskScores] = useState<RiskScore[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [emoryDashboard, setEmoryDashboard] = useState<HospitalDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [emoryLoading, setEmoryLoading] = useState(true)
  const [modalContent, setModalContent] = useState<{isOpen: boolean, title: string, content: React.ReactNode}>({
    isOpen: false,
    title: '',
    content: null
  })

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  useEffect(() => {
    loadData()
    // Refresh every 5 minutes
    const interval = setInterval(loadData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      const [riskData, alertsData] = await Promise.all([
        getLatestRiskScores(),
        getAlerts({ limit: 5, is_read: false })
      ])
      setRiskScores(riskData.scores || [])
      setAlerts(alertsData.alerts || [])
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }

    // Load Emory Hospital data
    try {
      setEmoryLoading(true)
      const emoryData = await getHospitalDashboard('emory-main', 1)
      setEmoryDashboard(emoryData)
    } catch (error) {
      console.error('Error loading Emory Hospital data:', error)
    } finally {
      setEmoryLoading(false)
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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'var(--color-red)'
      case 'high':
        return 'var(--color-orange)'
      case 'medium':
        return '#facc15'
      case 'low':
        return 'var(--color-gray)'
      default:
        return 'var(--color-gray)'
    }
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'critical':
        return 'var(--color-red)'
      case 'high':
        return 'var(--color-orange)'
      case 'medium':
        return '#fbbf24'
      case 'low':
        return '#e5e5e5'
      default:
        return '#e5e5e5'
    }
  }

  const openRiskScoreModal = (score: RiskScore) => {
    setModalContent({
      isOpen: true,
      title: `Risk Score Details - ${score.region_id}`,
      content: (
        <div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Region</div>
            <div className="modal-detail-value">{score.region_id}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Risk Level</div>
            <div className="modal-badge" style={{ backgroundColor: getRiskColor(score.risk_level), color: (score.risk_level === 'medium' || score.risk_level === 'low') ? '#000000' : '#ffffff' }}>
              {score.risk_level.toUpperCase()}
            </div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Risk Probability</div>
            <div className="modal-detail-value large">{formatPercentage(score.risk_probability)}</div>
          </div>
          <div className="modal-divider"></div>
          {score.contributing_factors && (
            <div className="modal-detail-row">
              <div className="modal-detail-label">Contributing Factors</div>
              <div className="modal-detail-value">{score.contributing_factors}</div>
            </div>
          )}
        </div>
      )
    })
  }

  const openAlertModal = (alert: Alert) => {
    setModalContent({
      isOpen: true,
      title: `Alert Details - ${alert.region_id}`,
      content: (
        <div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Region</div>
            <div className="modal-detail-value">{alert.region_id}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Severity</div>
            <div className="modal-badge" style={{ backgroundColor: getPriorityColor(alert.severity), color: (alert.severity === 'medium' || alert.severity === 'low') ? '#000000' : '#ffffff' }}>
              {alert.severity.toUpperCase()}
            </div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Alert Type</div>
            <div className="modal-detail-value">{alert.alert_type.replace('_', ' ').toUpperCase()}</div>
          </div>
          <div className="modal-divider"></div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Title</div>
            <div className="modal-detail-value">{alert.title}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Message</div>
            <div className="modal-detail-value">{alert.message}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Created</div>
            <div className="modal-detail-value">{new Date(alert.created_at).toLocaleString()}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Status</div>
            <div className="modal-detail-value">{alert.is_read ? 'Read' : 'Unread'}</div>
          </div>
        </div>
      )
    })
  }

  const openBudgetModal = (budget: any) => {
    setModalContent({
      isOpen: true,
      title: 'Budget Details',
      content: (
        <div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Total Budget</div>
            <div className="modal-detail-value large">{formatCurrency(budget.total)}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Allocated Budget</div>
            <div className="modal-detail-value">{formatCurrency(budget.allocated)}</div>
            <div style={{ color: '#737373', fontSize: '0.9rem', marginTop: '0.25rem' }}>{formatPercentage(budget.allocated / budget.total)} of total</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Available Budget</div>
            <div className="modal-detail-value">{formatCurrency(budget.available)}</div>
            <div style={{ color: '#737373', fontSize: '0.9rem', marginTop: '0.25rem' }}>{formatPercentage(budget.available / budget.total)} of total</div>
          </div>
          {budget.riskAdjusted && (
            <div className="modal-detail-row">
              <div className="modal-detail-label">Risk-Adjusted Budget</div>
              <div className="modal-detail-value" style={{ color: 'var(--color-red)' }}>{formatCurrency(budget.riskAdjusted)}</div>
            </div>
          )}
          <div className="modal-divider"></div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Period</div>
            <div className="modal-detail-value">{budget.period}</div>
          </div>
        </div>
      )
    })
  }

  const openResourceModal = (resource: any) => {
    setModalContent({
      isOpen: true,
      title: `Resource Allocation - ${resource.resource_type.toUpperCase()}`,
      content: (
        <div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Priority Level</div>
            <div className="modal-badge" style={{ backgroundColor: getPriorityColor(resource.priority_level), color: (resource.priority_level === 'medium' || resource.priority_level === 'low') ? '#000000' : '#ffffff' }}>
              {resource.priority_level.toUpperCase()}
            </div>
          </div>
          <div className="modal-divider"></div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Current Capacity</div>
            <div className="modal-detail-value large">{resource.current_capacity.toLocaleString()}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Recommended Capacity</div>
            <div className="modal-detail-value" style={{ color: 'var(--color-red)', fontSize: '1.5rem', fontWeight: 600 }}>{resource.recommended_capacity.toLocaleString()}</div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Utilization Rate</div>
            <div className="modal-detail-value">{formatPercentage(resource.utilization_rate)}</div>
          </div>
          <div className="modal-divider"></div>
          {resource.allocation_reason && (
            <div className="modal-detail-row">
              <div className="modal-detail-label">Recommendation Reason</div>
              <div className="modal-detail-value">{resource.allocation_reason}</div>
            </div>
          )}
        </div>
      )
    })
  }

  const openRecommendationModal = (rec: any) => {
    setModalContent({
      isOpen: true,
      title: rec.title,
      content: (
        <div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Priority</div>
            <div className="modal-badge" style={{ backgroundColor: getPriorityColor(rec.priority), color: (rec.priority === 'medium' || rec.priority === 'low') ? '#000000' : '#ffffff' }}>
              {rec.priority.toUpperCase()}
            </div>
          </div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Type</div>
            <div className="modal-detail-value">{rec.recommendation_type.toUpperCase()}</div>
          </div>
          <div className="modal-divider"></div>
          <div className="modal-detail-row">
            <div className="modal-detail-label">Description</div>
            <div className="modal-detail-value">{rec.description}</div>
          </div>
          {rec.estimated_impact && (
            <div className="modal-detail-row">
              <div className="modal-detail-label">Estimated Impact</div>
              <div className="modal-detail-value">{rec.estimated_impact}</div>
            </div>
          )}
          <div className="modal-divider"></div>
          {(rec.estimated_cost || rec.estimated_savings) && (
            <div>
              {rec.estimated_cost && (
                <div className="modal-detail-row">
                  <div className="modal-detail-label">Estimated Cost</div>
                  <div className="modal-detail-value" style={{ color: '#ea580c' }}>{formatCurrency(rec.estimated_cost)}</div>
                </div>
              )}
              {rec.estimated_savings && (
                <div className="modal-detail-row">
                  <div className="modal-detail-label">Annual Savings</div>
                  <div className="modal-detail-value" style={{ color: '#16a34a' }}>{formatCurrency(rec.estimated_savings)}</div>
                </div>
              )}
              <div className="modal-divider"></div>
            </div>
          )}
          {rec.timeframe && (
            <div className="modal-detail-row">
              <div className="modal-detail-label">Timeframe</div>
              <div className="modal-detail-value">{rec.timeframe}</div>
            </div>
          )}
        </div>
      )
    })
  }

  const closeModal = () => {
    setModalContent({ isOpen: false, title: '', content: null })
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  const criticalRegions = riskScores.filter(
    (r) => r.risk_level === 'critical' || r.risk_level === 'high'
  )

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Dashboard</h1>

      <div className="dashboard-grid">
        {/* Overview Row - Risk and Alerts side by side */}
        <div className="overview-row">
          <div className="dashboard-section">
            <h2 className="section-title">Risk Overview</h2>
            <div className="risk-cards">
              {criticalRegions.length > 0 ? (
                criticalRegions.map((score) => (
                  <RiskScoreCard key={score.id} score={score} onClick={() => openRiskScoreModal(score)} />
                ))
              ) : (
                <div className="empty-state">No high-risk regions detected</div>
              )}
            </div>
          </div>

          <div className="dashboard-section">
            <h2 className="section-title">Recent Alerts</h2>
            <div className="alerts-list">
              {alerts.length > 0 ? (
                alerts.map((alert) => (
                  <AlertCard key={alert.id} alert={alert} onClick={() => openAlertModal(alert)} />
                ))
              ) : (
                <div className="empty-state">No active alerts</div>
              )}
            </div>
          </div>
        </div>

        {/* Emory Hospital Section */}
        {emoryDashboard && (
          <>
            <div className="dashboard-section full-width emory-header-section">
              <div className="emory-header-content">
                <h2 className="section-title">{emoryDashboard.facility_name}</h2>
                <p className="emory-subtitle">Integrated Health Intelligence Dashboard</p>
                {emoryDashboard.risk_score && (
                  <div className="emory-risk-badge" style={{ 
                    backgroundColor: emoryDashboard.risk_score.risk_level === 'critical' ? 'var(--color-red)' :
                                    emoryDashboard.risk_score.risk_level === 'high' ? 'var(--color-orange)' :
                                    emoryDashboard.risk_score.risk_level === 'medium' ? '#fbbf24' : '#e5e5e5',
                    color: emoryDashboard.risk_score.risk_level === 'medium' || emoryDashboard.risk_score.risk_level === 'low' ? '#000000' : '#ffffff',
                    padding: '0.5rem 1rem',
                    borderRadius: '6px',
                    display: 'inline-block',
                    marginTop: '0.5rem',
                    fontWeight: 600,
                    fontSize: '0.9rem'
                  }}>
                    <span>Regional Risk Level: {emoryDashboard.risk_score.risk_level.toUpperCase()} ({formatPercentage(emoryDashboard.risk_score.risk_probability)})</span>
                  </div>
                )}
              </div>
            </div>

            {/* Budget Overview */}
            {emoryDashboard.budget && (
              <div className="dashboard-section full-width">
                <h2 className="section-title">Budget Overview - {emoryDashboard.facility_name}</h2>
                <div className="budget-grid">
                  <div className="budget-card" style={{ cursor: 'pointer' }} onClick={() => openBudgetModal({ total: emoryDashboard.budget.total_budget, allocated: emoryDashboard.budget.allocated_budget, available: emoryDashboard.budget.available_budget, riskAdjusted: emoryDashboard.budget.risk_adjusted_budget, period: 'Quarterly Allocation' })}>
                    <div className="budget-label">Total Budget</div>
                    <div className="budget-value">{formatCurrency(emoryDashboard.budget.total_budget)}</div>
                    <div className="budget-period">Quarterly Allocation</div>
                  </div>
                  <div className="budget-card" style={{ cursor: 'pointer' }} onClick={() => openBudgetModal({ total: emoryDashboard.budget.total_budget, allocated: emoryDashboard.budget.allocated_budget, available: emoryDashboard.budget.available_budget, riskAdjusted: emoryDashboard.budget.risk_adjusted_budget, period: 'Quarterly Allocation' })}>
                    <div className="budget-label">Allocated</div>
                    <div className="budget-value">{formatCurrency(emoryDashboard.budget.allocated_budget)}</div>
                    <div className="budget-percentage">
                      {formatPercentage(emoryDashboard.budget.allocated_budget / emoryDashboard.budget.total_budget)}
                    </div>
                  </div>
                  <div className="budget-card" style={{ cursor: 'pointer' }} onClick={() => openBudgetModal({ total: emoryDashboard.budget.total_budget, allocated: emoryDashboard.budget.allocated_budget, available: emoryDashboard.budget.available_budget, riskAdjusted: emoryDashboard.budget.risk_adjusted_budget, period: 'Quarterly Allocation' })}>
                    <div className="budget-label">Available</div>
                    <div className="budget-value">{formatCurrency(emoryDashboard.budget.available_budget)}</div>
                    <div className="budget-percentage">
                      {formatPercentage(emoryDashboard.budget.available_budget / emoryDashboard.budget.total_budget)}
                    </div>
                  </div>
                  {emoryDashboard.budget.risk_adjusted_budget && (
                    <div className="budget-card" style={{ cursor: 'pointer' }} onClick={() => openBudgetModal({ total: emoryDashboard.budget.total_budget, allocated: emoryDashboard.budget.allocated_budget, available: emoryDashboard.budget.available_budget, riskAdjusted: emoryDashboard.budget.risk_adjusted_budget, period: 'Quarterly Allocation' })}>
                      <div className="budget-label">Risk-Adjusted Budget</div>
                      <div className="budget-value">{formatCurrency(emoryDashboard.budget.risk_adjusted_budget)}</div>
                      <div className="budget-note">Based on current risk level</div>
                    </div>
                  )}
                </div>
                {emoryDashboard.budget.recommended_allocation && (
                  <div className="recommendations-box">
                    <h3>Recommended Budget Adjustments</h3>
                    <div className="recommendations-list">
                      {Object.entries(emoryDashboard.budget.recommended_allocation).map(([category, rec]: [string, any]) => (
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
              </div>
            )}

            {/* Resource Allocations */}
            {emoryDashboard.resource_allocations.length > 0 && (
              <div className="dashboard-section full-width">
                <h2 className="section-title">Resource Allocation Recommendations</h2>
                <div className="resources-grid">
                  {emoryDashboard.resource_allocations.map((resource) => (
                    <div key={resource.id} className="resource-card" style={{ cursor: 'pointer' }} onClick={() => openResourceModal(resource)}>
                      <div className="resource-header">
                        <h3>{resource.resource_type.toUpperCase()}</h3>
                        <span
                          className="priority-badge"
                          style={{ 
                            backgroundColor: getPriorityColor(resource.priority_level), 
                            color: (resource.priority_level === 'medium' || resource.priority_level === 'low') ? '#000000' : '#ffffff', 
                            padding: '0.25rem 0.75rem', 
                            borderRadius: '12px', 
                            fontSize: '0.75rem',
                            fontWeight: 600
                          }}
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
                          <div className="metric-value recommended" style={{ color: 'var(--color-red)' }}>
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
                                backgroundColor: resource.utilization_rate > 0.8 ? 'var(--color-red)' : resource.utilization_rate > 0.6 ? 'var(--color-orange)' : '#10b981',
                                height: '8px',
                                borderRadius: '4px'
                              }}
                            />
                          </div>
                        </div>
                      </div>
                      {resource.allocation_reason && (
                        <div className="resource-reason" style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--color-gray-light)', fontSize: '0.85rem', color: 'var(--color-gray)', fontStyle: 'italic' }}>
                          {resource.allocation_reason}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {emoryDashboard.recommendations.length > 0 && (
              <div className="dashboard-section full-width">
                <h2 className="section-title">AI-Powered Recommendations</h2>
                <div className="recommendations-grid">
                  {emoryDashboard.recommendations.map((rec) => (
                    <div key={rec.id} className="recommendation-card" style={{ cursor: 'pointer' }} onClick={() => openRecommendationModal(rec)}>
                      <div className="rec-header">
                        <h3>{rec.title}</h3>
                        <div className="rec-badges">
                          <span
                            className="priority-badge"
                            style={{ 
                              backgroundColor: getPriorityColor(rec.priority), 
                              color: (rec.priority === 'medium' || rec.priority === 'low') ? '#000000' : '#ffffff', 
                              padding: '0.25rem 0.75rem', 
                              borderRadius: '12px', 
                              fontSize: '0.75rem', 
                              marginRight: '0.5rem',
                              fontWeight: 600
                            }}
                          >
                            {rec.priority}
                          </span>
                          <span className="type-badge" style={{ padding: '0.25rem 0.75rem', borderRadius: '12px', fontSize: '0.75rem', backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                            {rec.recommendation_type}
                          </span>
                        </div>
                      </div>
                      <p className="rec-description" style={{ color: 'var(--color-gray)', lineHeight: '1.6', marginBottom: '1rem' }}>
                        {rec.description}
                      </p>
                      {rec.estimated_impact && (
                        <div className="rec-impact" style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid var(--color-gray-light)', fontSize: '0.9rem' }}>
                          <strong>Impact:</strong> {rec.estimated_impact}
                        </div>
                      )}
                      <div className="rec-financials" style={{ display: 'flex', gap: '1.5rem', marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid var(--color-gray-light)', fontSize: '0.9rem', flexWrap: 'wrap' }}>
                        {rec.estimated_cost && (
                          <div className="rec-cost" style={{ color: '#fbbf24' }}>
                            <strong>Cost:</strong> {formatCurrency(rec.estimated_cost)}
                          </div>
                        )}
                        {rec.estimated_savings && (
                          <div className="rec-savings" style={{ color: '#10b981' }}>
                            <strong>Annual Savings:</strong> {formatCurrency(rec.estimated_savings)}
                          </div>
                        )}
                      </div>
                      {rec.timeframe && (
                        <div className="rec-timeframe" style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid var(--color-gray-light)', fontSize: '0.9rem' }}>
                          <strong>Timeframe:</strong> {rec.timeframe}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {emoryLoading && (
          <div className="dashboard-section full-width">
            <div className="empty-state">Loading Emory Hospital data...</div>
          </div>
        )}

        <div className="dashboard-section full-width">
          <h2 className="section-title">Risk Trends</h2>
          <TrendChart />
        </div>

        <div className="dashboard-section full-width">
          <h2 className="section-title">Horizon Assistant</h2>
          <HorizonAssistant
            context={{
              riskScores,
              alerts,
            }}
          />
        </div>
      </div>

      {/* Modal for detailed views */}
      <CardModal
        isOpen={modalContent.isOpen}
        onClose={closeModal}
        title={modalContent.title}
      >
        {modalContent.content}
      </CardModal>
    </div>
  )
}


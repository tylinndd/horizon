import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { getRiskScores } from '../services/api'
import './TrendChart.css'

interface RiskDataPoint {
  timestamp: string
  risk_probability: number
  region_id: string
}

export default function TrendChart() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTrendData()
  }, [])

  const loadTrendData = async () => {
    try {
      const endDate = new Date()
      const startDate = new Date()
      startDate.setDate(startDate.getDate() - 30) // Last 30 days

      const response = await getRiskScores({
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        limit: 1000
      })

      // Group by date and calculate average risk
      const grouped: { [key: string]: { count: number; total: number } } = {}
      
      response.scores?.forEach((score: RiskDataPoint) => {
        const date = new Date(score.timestamp).toISOString().split('T')[0]
        if (!grouped[date]) {
          grouped[date] = { count: 0, total: 0 }
        }
        grouped[date].count++
        grouped[date].total += score.risk_probability
      })

      const chartData = Object.entries(grouped)
        .map(([date, values]) => ({
          date,
          risk: (values.total / values.count) * 100
        }))
        .sort((a, b) => a.date.localeCompare(b.date))

      setData(chartData)
    } catch (error) {
      console.error('Error loading trend data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="chart-loading">Loading chart data...</div>
  }

  if (data.length === 0) {
    return <div className="chart-empty">No trend data available</div>
  }

  return (
    <div className="trend-chart">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
          <XAxis 
            dataKey="date" 
            stroke="#000"
            tick={{ fill: '#000' }}
            tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
          />
          <YAxis 
            stroke="#000"
            tick={{ fill: '#000' }}
            domain={[0, 100]}
            label={{ value: 'Risk %', angle: -90, position: 'insideLeft', fill: '#000' }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #000' }}
            labelStyle={{ color: '#000' }}
            formatter={(value: number) => `${value.toFixed(1)}%`}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="risk" 
            stroke="#dc2626" 
            strokeWidth={2}
            dot={{ fill: '#dc2626', r: 3 }}
            name="Average Risk"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}


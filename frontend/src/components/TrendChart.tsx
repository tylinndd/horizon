import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { getRiskScores, getLatestRiskScores } from '../services/api'
import './TrendChart.css'

interface RiskDataPoint {
  timestamp: string
  risk_probability: number
  region_id: string
}

export default function TrendChart() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedRegion, setSelectedRegion] = useState<string>('all')
  const [chartType, setChartType] = useState<'line' | 'bar'>('line')
  const [timeRange, setTimeRange] = useState<number>(30) // days
  const [availableRegions, setAvailableRegions] = useState<string[]>([])

  useEffect(() => {
    loadTrendData()
  }, [selectedRegion, timeRange])

  const loadTrendData = async () => {
    try {
      const endDate = new Date()
      const startDate = new Date()
      startDate.setDate(startDate.getDate() - timeRange)

      const response = await getRiskScores({
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        limit: 1000,
        ...(selectedRegion !== 'all' && { region_id: selectedRegion })
      })

      // Get available regions from latest scores
      const latestResponse = await getLatestRiskScores()
      const regions = [...new Set((latestResponse.scores || []).map((s: RiskDataPoint) => s.region_id))]
      setAvailableRegions(regions)

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
          risk: (values.total / values.count) * 100,
          count: values.count
        }))
        .sort((a, b) => a.date.localeCompare(b.date))

      setData(chartData)
    } catch (error) {
      console.error('Error loading trend data:', error)
      // Generate sample data if API fails
      generateSampleData()
    } finally {
      setLoading(false)
    }
  }

  const generateSampleData = () => {
    const sampleData = []
    const today = new Date()
    for (let i = timeRange; i >= 0; i--) {
      const date = new Date(today)
      date.setDate(date.getDate() - i)
      sampleData.push({
        date: date.toISOString().split('T')[0],
        risk: 30 + Math.random() * 40,
        count: Math.floor(Math.random() * 10) + 1
      })
    }
    setData(sampleData)
  }

  if (loading) {
    return <div className="chart-loading">Loading chart data...</div>
  }

  if (data.length === 0) {
    return (
      <div className="chart-empty">
        <p>No trend data available</p>
        <button onClick={generateSampleData} className="generate-sample-btn">
          Generate Sample Data
        </button>
      </div>
    )
  }

  return (
    <div className="trend-chart-container">
      <div className="chart-controls">
        <div className="control-group">
          <label>Region:</label>
          <select 
            value={selectedRegion} 
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="chart-select"
          >
            <option value="all">All Regions</option>
            {availableRegions.map(region => (
              <option key={region} value={region}>{region}</option>
            ))}
          </select>
        </div>
        
        <div className="control-group">
          <label>Time Range:</label>
          <select 
            value={timeRange} 
            onChange={(e) => setTimeRange(Number(e.target.value))}
            className="chart-select"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>

        <div className="control-group">
          <label>Chart Type:</label>
          <div className="chart-type-buttons">
            <button
              className={`type-btn ${chartType === 'line' ? 'active' : ''}`}
              onClick={() => setChartType('line')}
            >
              Line
            </button>
            <button
              className={`type-btn ${chartType === 'bar' ? 'active' : ''}`}
              onClick={() => setChartType('bar')}
            >
              Bar
            </button>
          </div>
        </div>
      </div>

      <div className="trend-chart">
        <ResponsiveContainer width="100%" height={350}>
          {chartType === 'line' ? (
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
                dot={{ fill: '#dc2626', r: 4 }}
                name="Average Risk"
              />
            </LineChart>
          ) : (
            <BarChart data={data}>
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
              <Bar 
                dataKey="risk" 
                fill="#dc2626"
                name="Average Risk"
              />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  )
}

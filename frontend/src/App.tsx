import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Alerts from './pages/Alerts'
import RiskMap from './pages/RiskMap'
import './App.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/map" element={<RiskMap />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App


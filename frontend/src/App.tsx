import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ScrollToTop from './components/ScrollToTop'
import Homepage from './pages/Homepage'
import Platform from './pages/Platform'
import Dashboard from './pages/Dashboard'
import Alerts from './pages/Alerts'
import './App.css'

function App() {
  return (
    <Router>
      <ScrollToTop />
      <Layout>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/platform" element={<Platform />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App


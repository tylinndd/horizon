import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <Link to="/" className="logo">
            <span className="logo-text">HORIZON</span>
          </Link>
          <nav className="nav">
            <Link
              to="/"
              className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
            >
              Dashboard
            </Link>
            <Link
              to="/map"
              className={`nav-link ${location.pathname === '/map' ? 'active' : ''}`}
            >
              Risk Map
            </Link>
            <Link
              to="/alerts"
              className={`nav-link ${location.pathname === '/alerts' ? 'active' : ''}`}
            >
              Alerts
            </Link>
          </nav>
        </div>
      </header>
      <main className="main-content">{children}</main>
    </div>
  )
}


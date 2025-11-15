import { ReactNode, useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const [isScrolled, setIsScrolled] = useState(false)
  const isHomepage = location.pathname === '/'
  const isPlatform = location.pathname === '/platform'

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="layout">
      <header className={`header ${isScrolled || (!isHomepage && !isPlatform) ? 'scrolled' : ''}`}>
        <div className="header-content">
          <Link to="/" className="logo">
            <span className="logo-text">HORIZON</span>
          </Link>
          <nav className="nav">
            <Link
              to="/platform"
              className={`nav-link ${location.pathname === '/platform' ? 'active' : ''}`}
            >
              Platform
            </Link>
            <Link
              to="/dashboard"
              className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
            >
              Dashboard
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
      <main className={isHomepage || isPlatform ? "main-content-homepage" : "main-content"}>{children}</main>
    </div>
  )
}


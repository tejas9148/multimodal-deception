import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { FiMenu, FiX, FiBell, FiUser } from 'react-icons/fi'

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const isDashboard = location.pathname === '/dashboard'

  const scrollToSection = (id) => {
    setMenuOpen(false)
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  const handleLogo = () => {
    if (isDashboard) {
      navigate('/')
    } else {
      navigate('/')
    }
  }

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-logo" onClick={handleLogo} style={{ cursor: 'pointer' }}>
          🛡️ Deceptra AI
        </div>
        
        {/* Mobile menu button */}
        <div className="mobile-menu-button" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
        </div>

        {/* Navigation Menu */}
        <div className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          {isDashboard ? (
            <>
              <button onClick={() => navigate('/dashboard')} className="nav-link active">Dashboard</button>
              <button onClick={() => navigate('/dashboard')} className="nav-link">Analyze</button>
              <button onClick={() => navigate('/dashboard')} className="nav-link">History</button>
              <button onClick={() => navigate('/dashboard')} className="nav-link">Settings</button>
            </>
          ) : (
            <>
              <button onClick={() => scrollToSection('hero')} className="nav-link">Home</button>
              <button onClick={() => scrollToSection('features')} className="nav-link">Features</button>
              <button onClick={() => scrollToSection('about')} className="nav-link">About</button>
              <button onClick={() => scrollToSection('contact')} className="nav-link">Contact</button>
            </>
          )}
        </div>

        {/* Right side icons and button */}
        <div className="nav-right">
          {isDashboard && (
            <>
              <button className="nav-icon-btn" title="Notifications">
                <FiBell size={20} />
              </button>
              <button className="nav-icon-btn" title="Profile">
                <FiUser size={20} />
              </button>
            </>
          )}
          {!isDashboard && <button className="nav-cta">Get Started</button>}
        </div>
      </div>
    </nav>
  )
}

export default Navbar

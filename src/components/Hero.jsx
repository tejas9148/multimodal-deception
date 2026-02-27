import { useNavigate } from 'react-router-dom'

function Hero() {
  const navigate = useNavigate()

  return (
    <section id="hero" className="hero-section">
      <div className="hero-container">
        <div className="hero-content">
          <h1 className="hero-title">
            Multimodal<br />Social Media<br /><span className="title-highlight">Deception<br />Detection</span>
          </h1>
          
          <p className="hero-subtitle">
            Harness real-time AI to identify misinformation and deepfakes across text, images, and video with unprecedented accuracy.
          </p>
          
          <div className="hero-buttons">
            <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>Try Now <span>→</span></button>
          </div>
        </div>

        {/* Hero Illustration - Dark Card with Analysis Dashboard */}
        <div className="hero-illustration">
          <div className="illustration-card">
            <div className="card-bg-gradient"></div>
            
            {/* Shield Icon */}
            <div className="shield-graphic">
              <svg viewBox="0 0 200 240" className="shield-icon-large">
                <defs>
                  <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{stopColor: '#3B82F6', stopOpacity: 1}} />
                    <stop offset="100%" style={{stopColor: '#2563EB', stopOpacity: 1}} />
                  </linearGradient>
                </defs>
                <path d="M100 20 L160 50 L160 130 Q160 180 100 210 Q40 180 40 130 L40 50 Z" 
                      fill="url(#shieldGrad)" opacity="0.95" stroke="url(#shieldGrad)" strokeWidth="2"/>
                <path d="M75 110 L95 135 L140 85" 
                      stroke="white" strokeWidth="12" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero

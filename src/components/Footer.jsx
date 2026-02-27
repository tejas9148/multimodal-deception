import { FiMail, FiGithub, FiTwitter, FiLinkedin } from 'react-icons/fi'

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section footer-brand">
          <div className="footer-logo">Deceptra AI</div>
          <p className="footer-description">
            Empowering individuals and organizations to verify truth through advanced AI analysis.
          </p>
          <div className="footer-socials">
            <a href="#" className="social-link"><FiGithub size={20} /></a>
            <a href="#" className="social-link"><FiTwitter size={20} /></a>
            <a href="#" className="social-link"><FiLinkedin size={20} /></a>
          </div>
        </div>

        <div className="footer-section">
          <h4 className="footer-title">Product</h4>
          <ul className="footer-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#how">How It Works</a></li>
            <li><a href="#">Pricing</a></li>
            <li><a href="#">API Documentation</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4 className="footer-title">Company</h4>
          <ul className="footer-links">
            <li><a href="#about">About Us</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Privacy Policy</a></li>
          </ul>
        </div>

        <div className="footer-section footer-newsletter">
          <h4 className="footer-title">Newsletter</h4>
          <p className="footer-text">Stay updated with the latest in AI security.</p>
          <div className="newsletter-form">
            <input type="email" placeholder="Enter your email" className="newsletter-input" />
            <button className="newsletter-btn"><FiMail size={18} /></button>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; 2026 Deceptra AI. All rights reserved.</p>
        <div className="footer-bottom-socials">
          <a href="#">@</a>
          <a href="#">🔗</a>
          <a href="#">⚙️</a>
        </div>
      </div>
    </footer>
  )
}

export default Footer

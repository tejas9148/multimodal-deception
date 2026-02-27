import { useNavigate } from 'react-router-dom'

function CTA() {
  const navigate = useNavigate()

  return (
    <section className="cta-section">
      <div className="cta-container">
        <h2 className="cta-title">Ready to detect deception?</h2>
        <p className="cta-subtitle">
          Start your free trial today.
        </p>
        <button className="btn btn-cta" onClick={() => navigate('/dashboard')}>Start Free Trial</button>
      </div>
    </section>
  )
}

export default CTA

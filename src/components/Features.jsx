import { FiFileText, FiImage, FiBarChart2 } from 'react-icons/fi'

function Features() {
  return (
    <section id="features" className="features-section">
      <div className="features-container">
        <h2 className="section-title">Core Features</h2>
        
        <div className="features-grid">
          {/* Feature Card 1 */}
          <div className="feature-card">
            <div className="feature-icon-wrapper">
              <FiFileText className="feature-icon" size={40} />
            </div>
            <h3 className="feature-title">Text Analysis</h3>
            <p className="feature-description">
              NLP-based detection of sensational and misleading content.
            </p>
          </div>

          {/* Feature Card 2 */}
          <div className="feature-card">
            <div className="feature-icon-wrapper">
              <FiImage className="feature-icon" size={40} />
            </div>
            <h3 className="feature-title">Image Risk Detection</h3>
            <p className="feature-description">
              Detect embedded text, meme patterns, and manipulated visuals.
            </p>
          </div>

          {/* Feature Card 3 */}
          <div className="feature-card">
            <div className="feature-icon-wrapper">
              <FiBarChart2 className="feature-icon" size={40} />
            </div>
            <h3 className="feature-title">Fusion Risk Scoring</h3>
            <p className="feature-description">
              Combine multimodal insights into an explainable deception score.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Features

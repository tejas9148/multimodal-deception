import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FiZap, FiType, FiImage, FiDatabase, FiLayers, FiHelpCircle } from 'react-icons/fi'

function Dashboard() {
  const navigate = useNavigate()
  const [textContent, setTextContent] = useState('')
  const [selectedImage, setSelectedImage] = useState(null)
  const [metadata, setMetadata] = useState({
    followers: false,
    accountAge: false,
    engagementRate: false
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [riskScore, setRiskScore] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)

  const handleAnalyze = async () => {
    // Validation
    if (!textContent.trim()) {
      setError('Please enter content to analyze')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Prepare form data for multimodal analysis
      const formData = new FormData()
      formData.append('text', textContent)
      
      // Add image if selected
      if (selectedImage) {
        formData.append('image', selectedImage)
      }

      // Add metadata if selected
      if (metadata.followers) formData.append('followers', true)
      if (metadata.accountAge) formData.append('accountAge', true)
      if (metadata.engagementRate) formData.append('engagementRate', true)

      // Use real backend API endpoint
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      if (response.ok) {
        setRiskScore(data.riskScore)
        setAnalysisResult({
          risk: data.riskScore > 70 ? 'HIGH RISK' : data.riskScore > 40 ? 'MEDIUM RISK' : 'LOW RISK',
          score: data.riskScore,
          verdict: data.verdict,
          text: data.textScore,
          image: data.imageScore,
          trust: data.trustScore,
          reasons: Array.isArray(data.reasons) ? data.reasons.map(r => typeof r === 'string' ? { title: r, description: r } : r) : []
        })
      } else {
        setError(data.error || 'Analysis failed. Please try again.')
      }
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.')
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
    }
  }

  const analysisFeatures = [
    { icon: FiType, label: 'TEXT INTELLIGENCE' },
    { icon: FiImage, label: 'IMAGE RISK' },
    { icon: FiDatabase, label: 'METADATA ANALYSIS' },
    { icon: FiLayers, label: 'FUSION SCORING' },
    { icon: FiHelpCircle, label: 'EXPLAINABLE AI' }
  ]

  // TODO: Replace with real data fetched from backend
  const recentAnalysis = [
    { date: 'Oct 24 2023 14:20', content: 'Breaking: New policy chang...', risk: 87, status: 'FLAGGED' },
    { date: 'Oct 23 2023 09:15', content: 'How to build a sustainable g...', risk: 15, status: 'VERIFIED' },
    { date: 'Oct 22 2023 18:45', content: 'The local library will be host...', risk: 45, status: 'SUSPECT' }
  ]

  const getRiskColor = (score) => {
    if (score > 70) return '#EF4444'
    if (score > 40) return '#F59E0B'
    return '#10B981'
  }

  return (
    <section className="dashboard-section">
      <div className="dashboard-container">
        {/* Header */}
        <div className="dashboard-header">
          <h1>Deception Analysis Dashboard</h1>
          <p>Analyze social media posts using multimodal AI for veracity and risk detection.</p>
        </div>

        {/* Main Content Grid */}
        <div className="dashboard-grid">
          {/* Left Panel - Content Analysis */}
          <div className="content-analysis-panel">
            <div className="panel-header">
              <div className="panel-icon">📋</div>
              <h2>Content Analysis</h2>
            </div>

            <div className="form-section">
              <label className="form-label">Social Media Content</label>
              <textarea
                className="content-textarea"
                placeholder="Paste the post text, tweet, or article content here for analysis..."
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
              />
            </div>

            {/* Drop Image Section */}
            <div className="drop-image-area">
              <input
                type="file"
                id="image-input"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
              />
              <label htmlFor="image-input" style={{ cursor: 'pointer', width: '100%' }}>
                <div className="drop-image-content">
                  <p className="drop-label">📸 {selectedImage ? selectedImage.name : 'DROP IMAGE HERE'}</p>
                  <p className="drop-hint">PNG, JPG or WEBP (Max 50MB)</p>
                </div>
              </label>
            </div>

            {/* Metadata Section */}
            <div className="metadata-section">
              <p className="metadata-title">METADATA INPUTS</p>
              <div className="metadata-items">
                <label className="metadata-item">
                  <input 
                    type="checkbox" 
                    checked={metadata.followers}
                    onChange={(e) => setMetadata({...metadata, followers: e.target.checked})}
                  />
                  <span>Followers (e.g. 15k)</span>
                </label>
                <label className="metadata-item">
                  <input 
                    type="checkbox"
                    checked={metadata.accountAge}
                    onChange={(e) => setMetadata({...metadata, accountAge: e.target.checked})}
                  />
                  <span>Account Age (e.g. 2y)</span>
                </label>
                <label className="metadata-item">
                  <input 
                    type="checkbox"
                    checked={metadata.engagementRate}
                    onChange={(e) => setMetadata({...metadata, engagementRate: e.target.checked})}
                  />
                  <span>Engagement Rate (%)</span>
                </label>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div style={{
                padding: '1rem',
                marginBottom: '1rem',
                background: '#FEE2E2',
                border: '1px solid #FECACA',
                borderRadius: '0.75rem',
                color: '#991B1B',
                fontSize: '0.9rem'
              }}>
                {error}
              </div>
            )}

            {/* Analyze Button */}
            <button 
              className="analyze-button" 
              onClick={handleAnalyze}
              disabled={loading}
              style={{ opacity: loading ? 0.7 : 1, cursor: loading ? 'not-allowed' : 'pointer' }}
            >
              <FiZap size={20} />
              {loading ? 'Analyzing...' : 'Analyze Content'}
            </button>

            {/* Analysis Features */}
            <div className="analysis-features">
              {analysisFeatures.map((feature, idx) => (
                <div key={idx} className="feature-icon-btn" title={feature.label}>
                  <feature.icon size={24} />
                  <span className="feature-label">{feature.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Panel - Analysis Results */}
          <div className="results-panel">
            {analysisResult ? (
              <>
                {/* Risk Badge */}
                <div className="risk-badge">
                  <span className="badge-high">HIGH RISK</span>
                </div>

                {/* Circular Progress */}
                <div className="result-circle">
                  <svg className="progress-ring" width="200" height="200">
                    <circle
                      cx="100"
                      cy="100"
                      r="90"
                      fill="none"
                      stroke="rgba(229, 231, 235, 0.1)"
                      strokeWidth="8"
                    />
                    <circle
                      cx="100"
                      cy="100"
                      r="90"
                      fill="none"
                      stroke={getRiskColor(riskScore)}
                      strokeWidth="8"
                      strokeDasharray={`${(riskScore / 100) * 565} 565`}
                      style={{ transform: 'rotate(-90deg)', transformOrigin: '100px 100px' }}
                    />
                  </svg>
                  <div className="circle-content">
                    <p className="result-percentage">{riskScore}%</p>
                    <p className="result-verdict">DECEPTIVE</p>
                  </div>
                </div>

                <p className="result-text">
                  This content shows significant markers of manipulation and deceptive intent.
                </p>

                {/* Score Stats */}
                <div className="score-stats">
                  <div className="stat">
                    <p className="stat-label">TEXT</p>
                    <p className="stat-value">{analysisResult.text}%</p>
                  </div>
                  {typeof analysisResult.image !== 'undefined' && (
                    <div className="stat">
                      <p className="stat-label">IMAGE</p>
                      <p className="stat-value">{analysisResult.image}%</p>
                    </div>
                  )}
                  {typeof analysisResult.trust !== 'undefined' && (
                    <div className="stat">
                      <p className="stat-label">TRUST</p>
                      <p className="stat-value">{analysisResult.trust}%</p>
                    </div>
                  )}
                </div>

                {/* Why This Is Flagged */}
                <div className="flagged-section">
                  <h3>⚠️ Why This Is Flagged</h3>
                  <ul className="flagged-list">
                    {analysisResult.reasons && analysisResult.reasons.map((reason, idx) => (
                      <li key={idx}>
                        <strong>{reason.title}</strong>
                        <p>{reason.description}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <div className="results-placeholder">
                <p style={{ color: '#4B5563', textAlign: 'center', fontSize: '1rem' }}>Results will appear here</p>
              </div>
            )}
          </div>
        </div>

        {/* No Results Message */}
        {!analysisResult && (
          <div className="no-results-message">
            <p className="no-results-icon">📊</p>
            <p className="no-results-text">Submit content to see analysis results</p>
          </div>
        )}

        {/* Recent Analysis History */}
        <div className="history-section">
          <div className="history-header">
            <h2>Recent Analysis History</h2>
            <button className="view-all-btn">View All History →</button>
          </div>

          <div className="history-table">
            <div className="table-header">
              <div className="table-cell date-col">DATE</div>
              <div className="table-cell content-col">CONTENT PREVIEW</div>
              <div className="table-cell risk-col">RISK SCORE</div>
              <div className="table-cell status-col">STATUS</div>
              <div className="table-cell action-col">ACTION</div>
            </div>

            {recentAnalysis.map((item, idx) => (
              <div key={idx} className="table-row">
                <div className="table-cell date-col">{item.date}</div>
                <div className="table-cell content-col">{item.content}</div>
                <div className="table-cell risk-col">
                  <div className="risk-bar">
                    <div className="risk-fill" style={{ width: `${item.risk}%`, backgroundColor: getRiskColor(item.risk) }}></div>
                  </div>
                  <span>{item.risk}%</span>
                </div>
                <div className="table-cell status-col">
                  <span className={`status-badge status-${item.status.toLowerCase()}`}>
                    {item.status}
                  </span>
                </div>
                <div className="table-cell action-col">
                  <button className="view-details-btn">View Details</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default Dashboard

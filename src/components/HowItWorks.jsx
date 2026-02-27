import { FiUploadCloud, FiCpu, FiShield } from 'react-icons/fi'

function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Upload Content',
      description: 'Drag and drop URLs & text blocks or images directly into our dashboard.',
      icon: FiUploadCloud,
      color: 'step-upload'
    },
    {
      number: '02',
      title: 'Multimodal Analysis',
      description: 'Our AI engine processes the content through specialized neural networks simultaneously.',
      icon: FiCpu,
      color: 'step-analysis'
    },
    {
      number: '03',
      title: 'Get Deception Score',
      description: 'Receive a comprehensive report with a risk score and detailed detection evidence.',
      icon: FiShield,
      color: 'step-score'
    }
  ]

  return (
    <section className="how-it-works-section">
      <div className="how-it-works-container">
        <h2 className="section-title">How It Works</h2>
        <p className="section-subtitle">Three simple steps to secure your digital presence.</p>
        
        <div className="steps-grid">
          {steps.map((step, index) => {
            const IconComponent = step.icon
            return (
              <div key={index} className={`step-card ${step.color}`}>
                <div className="step-number">STEP {step.number}</div>
                <div className="step-icon-wrapper">
                  <IconComponent size={48} className="step-icon" />
                </div>
                <h3 className="step-title">{step.title}</h3>
                <p className="step-description">{step.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default HowItWorks

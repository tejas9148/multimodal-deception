import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Features from './components/Features'
import HowItWorks from './components/HowItWorks'
import CTA from './components/CTA'
import About from './components/About'
import Footer from './components/Footer'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div className="app">
            <Navbar />
            <Hero />
            <Features />
            <HowItWorks />
            <CTA />
            <About />
            <Footer />
          </div>
        } />
        <Route path="/dashboard" element={
          <div className="app">
            <Navbar />
            <Dashboard />
            <Footer />
          </div>
        } />
      </Routes>
    </Router>
  )
}

export default App

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './EmotionDetector.jsx'
import VirtualDoctor from './virtualDr.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <VirtualDoctor />
  </StrictMode>,
)

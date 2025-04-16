import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { SocketProvider } from './contexts/socketContext.jsx'
import { UserProvider } from './contexts/userContext.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <UserProvider>
      <App />
   </UserProvider>
  </StrictMode>,
)

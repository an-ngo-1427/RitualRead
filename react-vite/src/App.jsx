import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import LobbyPage from './components/lobbyPage/LobbyPage'
import RoomPage from './components/roomPage/roomPage'
import LoginPage from './components/auth/LoginPage'
import './App.css'
import SignUpPage from './components/auth/SignUpPage'
import Layout from './Layout'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/lobby" />} />
          <Route path="lobby" element={<LobbyPage />} />
          <Route path="rooms/:roomId" element={<RoomPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="signup" element={<SignUpPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App

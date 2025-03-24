import { Outlet, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './Layout.css';

function Layout() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    // This is a placeholder - implement actual auth check
    const checkAuth = async () => {
        const response = await fetch('/api/auth/');
        if (response.ok) {
          setIsLoggedIn(true);
        }else{
          setIsLoggedIn(false)
        }
      }

    checkAuth();
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <Link to="/">Ritual Read</Link>
        </div>
        <nav className="main-nav">
          <Link to="/lobby" className="nav-link">Lobby</Link>
          {isLoggedIn ? (
            <button
              className="auth-button"
              onClick={async () => {
                await fetch('/api/auth/logout', { method: 'GET' });
                setIsLoggedIn(false);
              }}
            >
              Logout
            </button>
          ) : (
            <Link to="/login" className="auth-button">Login</Link>
          )}
        </nav>
      </header>

      <main className="app-content">
        <Outlet />
      </main>

      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} Ritual Read - All rights reserved</p>
      </footer>
    </div>
  );
}

export default Layout;

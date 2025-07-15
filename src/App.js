import { BrowserRouter as Router, Routes, Route} from 'react-router';
import 'leaflet/dist/leaflet.css';
import MainPage from './assets/MainPage';
import PhotoSubmitPage from './assets/PhotoSubmitPage';
import Rent from './assets/Rent';
import Auth from './assets/Auth';
import MapPage from './assets/MapPage';
import './App.css';
import { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './assets/firebase';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setIsLoggedIn(!!user);
    });
    return () => unsubscribe();
  }, []);
  return (
    <Router>
      <div>
        <nav className="navbar">
          <h1 className="navbar-title">Maizuru Bike Rental</h1>
            {isLoggedIn && (
            <div className="navbar-links">
              <button
                onClick={() => window.history.back()}
                className="navbar-back-button"
              >
                ← Back
              </button>
            </div>
          )}
        </nav>
        <Routes>
          <Route path="/" element={<Auth setIsLoggedIn={setIsLoggedIn} />} />
          <Route
            path="/home"
            element={<MainPage setIsLoggedIn={setIsLoggedIn} />}
          />
          <Route
            path="/map"
            element={<MapPage setIsLoggedIn={setIsLoggedIn} />}
          />
          <Route
            path="/submit"
            element={<PhotoSubmitPage setIsLoggedIn={setIsLoggedIn} />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

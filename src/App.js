import { BrowserRouter as Router, Routes, Route, Link } from 'react-router';
import 'leaflet/dist/leaflet.css';
import MainPage from './assets/MainPage';
import PhotoSubmitPage from './assets/PhotoSubmitPage';
import Auth from './assets/Auth';
import MapPage from './assets/MapPage';
import './App.css';
import { useState } from 'react';

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <Router>
      <div>
        <nav className="navbar">
          <h1 className="navbar-title">Maizuru Bike Rental</h1>
          {isLoggedIn && (
            <div className="navbar-links">
              <Link to="/home">Home</Link>
              <Link to="/map">Map</Link>
              <Link to="/submit-photo">Submit Photo</Link>
            </div>
          )}
        </nav>
        <Routes>
          <Route path="/" element={<Auth />} />
          <Route path="/home" element={<MainPage />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/submit" element={<PhotoSubmitPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
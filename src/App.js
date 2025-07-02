import { BrowserRouter as Router, Routes, Route} from 'react-router';
import 'leaflet/dist/leaflet.css';
import MainPage from './assets/MainPage';
import PhotoSubmitPage from './assets/PhotoSubmitPage';
import Rent from './assets/Rent';
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
              <button
                onClick={() => window.history.back()}
                className="navbar-back-button"
                >
                ← Back
              </button>
            </div>)}
        </nav>
        <Routes>
          <Route path="/" element={<Auth setIsLoggedIn={setIsLoggedIn}/>} />
          <Route path="/home" element={<MainPage />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/submit" element={<PhotoSubmitPage />} />
          <Route path="/rent" element={<Rent />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
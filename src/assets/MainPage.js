import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut, onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import './MainPage.css'; // Make sure this path matches your file structure

function MainPage({ setIsLoggedIn }) {
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (!user) {
        navigate('/');
      }
    });
    return () => unsubscribe();
  }, [navigate]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      setIsLoggedIn(false);
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <div className="main-container">
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderBottom: '2px solid #ddd',
          paddingBottom: '15px',
          marginBottom: '30px',
        }}
      >
        <h2 className="main-title">🚲 Maizuru Bike Rental</h2>

        <button
          onClick={handleLogout}
          className="logout-button"
          onMouseOver={(e) =>
            (e.currentTarget.style.backgroundColor = '#e04343')
          }
          onMouseOut={(e) =>
            (e.currentTarget.style.backgroundColor = '#ff4d4d')
          }
        >
          Log Out
        </button>
      </div>

      <p className="main-text">
        Explore Maizuru with our convenient bike rental service. Check available
        bikes on the map, and don’t forget to submit a photo after your ride!
      </p>

      <div className="button-group">
        <button
          className="action-button rent"
          onClick={() => navigate('/submit')}
        >
          Rent a Bike
        </button>
        <button className="action-button map" onClick={() => navigate('/map')}>
          Maps
        </button>
      </div>
    </div>
  );
}

export default MainPage;

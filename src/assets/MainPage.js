import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut, onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';

function MainPage() {
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
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <div className="container" style={{ padding: '40px', fontFamily: 'Arial, sans-serif' }}>
      {/* Header */}
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
        <h2
          className="main-title"
          style={{
            fontSize: '28px',
            color: '#333',
            margin: 0,
          }}
        >
          🚲 Maizuru Bike Rental
        </h2>

        <button
  onClick={handleLogout}
  style={{
    backgroundColor: '#ff4d4d',
    color: '#fff',
    border: 'none',
    padding: '6px 12px',
    fontSize: '13px',
    fontWeight: 500,
    borderRadius: '6px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease-in-out',
    width: '80px'

  }}
  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#e04343')}
  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#ff4d4d')}
>
  Log Out
</button>


      </div>

      {/* Main content */}
      <p
        className="main-text"
        style={{
          fontSize: '18px',
          color: '#444',
          lineHeight: '1.6',
        }}
      >
        Explore Maizuru with our convenient bike rental service. Check available bikes on the map,
        and don’t forget to submit a photo after your ride!
      </p>
    </div>
  );
}

export default MainPage;

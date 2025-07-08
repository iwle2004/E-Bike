import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Rent.css';
import {
  ref,
  uploadBytes,
  getDownloadURL,
  deleteObject,
} from 'firebase/storage';
import { storage } from './firebase.js'; // adjust if your path differs

function Rent() {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!file) {
      alert('Please select a photo before submitting.');
      return;
    }

    try {
      const storagePath = `uploads/${Date.now()}_${file.name}`;
      const storageRef = ref(storage, storagePath);

      console.log('Uploading...');
      await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(storageRef);
      console.log('✅ Uploaded:', downloadURL);
      const baseUrl =
        'https://e-bike-backend-hj9l.onrender.com/' || 'http://localhost:5000';

      // Send to Flask backend for detection
      const response = await fetch(`${baseUrl}/run-detection`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          downloadURL,
          storagePath,
        }),
      });

      const data = await response.json();

      // Delete the file after detection
      try {
        await deleteObject(storageRef);
        console.log('✅ Deleted photo from Firebase.');
      } catch (deleteError) {
        console.error('⚠️ Failed to delete photo:', deleteError);
      }

      if (data.status === 'success') {
        if (data.is_target_met) {
          navigate('/submit'); // page for "detection passed"
        } else {
          alert('QRコードをきれいに撮影お願いします');
          navigate('/rent'); // page for "detection failed"
        }
      } else {
        alert('Detection failed: ' + data.message);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="photo-submit-container">
      <h2 className="photo-submit-title">ArUcoマーカーを撮影してください</h2>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="photo-input"
      />
      <br />
      <div className="example-box">
        <p className="example-title">撮影例</p>
        <img src="./satsuei.jpg" alt="撮影例" className="example-image" />
      </div>
      <button onClick={handleSubmit} className="photo-button">
        SUBMIT
      </button>
    </div>
  );
}

export default Rent;

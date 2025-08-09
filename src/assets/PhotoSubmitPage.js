import { useState, useEffect } from 'react';
import './PhotoSubmitPage.css';
import { useNavigate } from 'react-router-dom';
import {
  ref,
  uploadBytes,
  getDownloadURL,
  deleteObject,
} from 'firebase/storage';
import { doc, setDoc } from 'firebase/firestore';
import { onAuthStateChanged } from 'firebase/auth';
import { storage, auth, db } from './firebase.js';

function PhotoSubmitPage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [userEmail, setUserEmail] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        setUserEmail(user.email);
      }
    });
    return () => unsubscribe();
  }, []);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      setPreviewUrl(URL.createObjectURL(selectedFile));
    } else {
      setPreviewUrl(null);
    }
  };

  const saveLocationToFirestore = async () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        return reject(new Error('Geolocation not supported'));
      }

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const lat = position.coords.latitude;
          const long = position.coords.longitude;

          if (!userEmail) {
            return reject(new Error('No user email found'));
          }

          try {
            await setDoc(doc(db, 'locations', userEmail), {
              email: userEmail,
              latitude: lat,
              longitude: long,
              timestamp: new Date(),
            });
            console.log('📍 Location saved for', userEmail);
            resolve();
          } catch (err) {
            reject(err);
          }
        },
        (err) => reject(err)
      );
    });
  };

  const handleSubmit = async () => {
    if (!file) {
      alert('Please select a photo before submitting.');
      return;
    }

    try {
      await saveLocationToFirestore();
      const storagePath = `uploads/${Date.now()}_${file.name}`;
      const storageRef = ref(storage, storagePath);

      console.log('Uploading...');
      await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(storageRef);
      console.log('✅ Uploaded:', downloadURL);
      const baseUrl =
        'https://e-bike-backend-lztz.onrender.com' || 'http://localhost:5000';

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
          navigate('/home'); // page for "detection passed"
        } else {
          alert('QRコードをきれいに撮影お願いします');
          navigate('/submit'); // page for "detection failed"
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
      <h2 className="photo-submit-title">Submit a Photo</h2>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="photo-input"
      />
      {previewUrl && (
        <div className="preview-container">
          <p>Preview:</p>
          <img src={previewUrl} alt="Preview" className="photo-preview" />
        </div>
      )}

      {/* 撮影例 box below */}
      <div className="example-box">
        <p className="example-title">撮影例</p>
        <div className="example-images-container">
          <img
            src="./iishashin.jpeg"
            alt="撮影例111"
            className="example-image"
          />
          <img
            src="./dameshashin.jpeg"
            alt="撮影例2"
            className="example-image"
          />
        </div>
      </div>

      <br />
      <button onClick={handleSubmit} className="photo-button">
        Submit Photo
      </button>
    </div>
  );
}

export default PhotoSubmitPage;

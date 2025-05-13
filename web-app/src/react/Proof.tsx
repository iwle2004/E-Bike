import React, { useState, useEffect } from 'react';
import Top from './Top.tsx';
import { Route, Routes } from 'react-router-dom';
import BluetoothComponent from './BluetoothComponent';
import UpdateFirestoreDocument from './UpdateFirestoreDocument';
import CustomButton from './CustomButton';
import { Box, Card, CardContent, Typography } from '@mui/material';
import NavigationIcon from '@mui/icons-material/Navigation';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import logo from '../images/logo.png';
import './Proof.css';
import FirestoreData from './FirestoreData';
import { useKeyStateContext } from '../context/KeyStateContext';
import { useDocumentContext } from '../context/DocumentContext'; // 追加
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Proof: React.FC = () => {
    // const { keyState } = useKeyStateContext();
    // const { selectedDocumentId } = useDocumentContext(); // useDocumentContext を使用
    // const [locked, setLocked] = useState<boolean | null>(null);
  
    // useEffect(() => {
    //   if (!selectedDocumentId) {
    //     // selectedDocumentId が空の場合、locked を null にリセット
    //     setLocked(null);
    //   } else {
    //     setLocked(keyState);
    //   }
    // }, [selectedDocumentId, keyState]);
  
    // const getCardContent = () => {
    //   if (locked === null) {
    //     return (
    //       <Typography variant="h6" className="centered-text">
    //         <div>場所を選択</div>
    //         <div>してください</div>
    //       </Typography>
    //     );
    //   } else {
    //     return (
    //       <>
    //         {locked ? <LockOpenIcon style={{ fontSize: 48, color: 'white' }} /> : <LockIcon style={{ fontSize: 48, color: 'white' }} />}
    //         <Typography variant="h6" style={{ marginTop: 8, color: 'white' }}>
    //           {locked ? "解錠中" : "施錠中"}
    //         </Typography>
    //       </>
    //     );
    //   }
    // };
    const [image, setImage] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setImage(file);
            setPreview(URL.createObjectURL(file));
        }
    };

  const handleSubmit = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await axios.post("/api/verify-dropoff", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { properly_parked, reason } = response.data;

      if (properly_parked) {
        alert("✅ Scooter drop-off confirmed. Thank you!");
        navigate("/ride-summary");
      } else {
        alert(`❌ Drop-off invalid: ${reason}. Please re-park and try again.`);
      }
    } catch (err) {
      console.error(err);
      alert("Error verifying image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="card">
        <h1 className="title">📍 Confirm Drop-off Location</h1>
        <p className="description">
          Please upload a photo of your parked scooter. Make sure it’s in a designated area and not blocking sidewalks or doors.
        </p>

        {preview && <img src={preview} alt="Preview" className="preview" />}

        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="file-input"
        />

        <button
          onClick={handleSubmit}
          disabled={loading || !image}
          className="submit-button"
        >
          {loading ? "Verifying..." : "Submit Photo"}
        </button>

        <button
          onClick={() => navigate("/")}
          className="back-button"
        >
          Go Back
        </button>
      </div>
    </div>
  );

    // return (
    //    <Box className="container">
    //    <img src={logo} alt="ME-Bike Logo" className="logo" />
  
    //    <Box className="split-container">
    //        <Card className="card">
    //          <CardContent className="card-content">
    //            <BluetoothComponent />
    //          </CardContent>
    //        </Card>
    //      </Box>
    //      <Box className="split-container">
    //        <Card className="card">
    //          <CardContent className="card-content">
    //            <CustomButton
    //              variant="contained"
    //              color="primary"
    //              icon={<NavigationIcon />}
    //              text="道案内"
    //              to="/map"
    //            />
    //          </CardContent>
    //        </Card>
    //      </Box>
        
    //      <Box className="split-container">
    //        <Card className="card half-width">
    //          <CardContent className="card-content">
    //            <UpdateFirestoreDocument />
    //          </CardContent>
    //       </Card>
  
    //        <Card
    //          className="card half-width"
    //         style={{ backgroundColor: locked === null ? '#9e9e9e' : (locked ? '#2196f3' : '#f44336') }}
    //        >
    //          <CardContent className="card-content">
    //            {getCardContent()}
    //          </CardContent>
    //        </Card>
    //      </Box>
  
    //      <FirestoreData />
    //    </Box>
    //  );
  };
  
  export default Proof;
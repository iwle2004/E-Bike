import React, { useState, useEffect } from 'react';
import BluetoothComponent from './BluetoothComponent';
import UpdateFirestoreDocument from './UpdateFirestoreDocument';
import CustomButton from './CustomButton';
import { Box, Card, CardContent, Typography } from '@mui/material';
import NavigationIcon from '@mui/icons-material/Navigation';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import logo from '../images/logo.png';
import './Top.css';
import FirestoreData from './FirestoreData';
import { useKeyStateContext } from '../context/KeyStateContext';
import { useDocumentContext } from '../context/DocumentContext'; // 追加

const Top: React.FC = () => {
  const { keyState } = useKeyStateContext();
  const { selectedDocumentId } = useDocumentContext(); // useDocumentContext を使用
  const [locked, setLocked] = useState<boolean | null>(null);

  useEffect(() => {
    if (!selectedDocumentId) {
      // selectedDocumentId が空の場合、locked を null にリセット
      setLocked(null);
    } else {
      setLocked(keyState);
    }
  }, [selectedDocumentId, keyState]);

  const getCardContent = () => {
    if (locked === null) {
      return (
        <Typography variant="h6" className="centered-text">
          <div>場所を選択</div>
          <div>してください</div>
        </Typography>
      );
    } else {
      return (
        <>
          {locked ? <LockOpenIcon style={{ fontSize: 48, color: 'white' }} /> : <LockIcon style={{ fontSize: 48, color: 'white' }} />}
          <Typography variant="h6" style={{ marginTop: 8, color: 'white' }}>
            {locked ? "解錠中" : "施錠中"}
          </Typography>
        </>
      );
    }
  };

  return (
    <Box className="container">
      <img src={logo} alt="ME-Bike Logo" className="logo" />

      <Box className="split-container">
        <Card className="card">
          <CardContent className="card-content">
            <BluetoothComponent />
          </CardContent>
        </Card>
      </Box>
      <Box className="split-container">
        <Card className="card">
          <CardContent className="card-content">
            <CustomButton
              variant="contained"
              color="primary"
              icon={<NavigationIcon />}
              text="道案内"
              to="/map"
            />
          </CardContent>
        </Card>
      </Box>
      
      <Box className="split-container">
        <Card className="card half-width">
          <CardContent className="card-content">
            <UpdateFirestoreDocument />
          </CardContent>
        </Card>

        <Card
          className="card half-width"
          style={{ backgroundColor: locked === null ? '#9e9e9e' : (locked ? '#2196f3' : '#f44336') }}
        >
          <CardContent className="card-content">
            {getCardContent()}
          </CardContent>
        </Card>
      </Box>

      <FirestoreData />
    </Box>
  );
};

export default Top;

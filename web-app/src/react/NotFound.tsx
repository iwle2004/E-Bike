// src/react/NotFound.tsx
import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import './NotFound.css';

const NotFound: React.FC = () => {
  return (
    <Box className="not-found-container">
      <Typography variant="h1" className="not-found-title">404</Typography>
      <Typography variant="h6" className="not-found-subtitle">ページが見つかりません</Typography>
      <Button variant="contained" color="primary" component={Link} to="/">
        ホームに戻る
      </Button>
    </Box>
  );
};

export default NotFound;

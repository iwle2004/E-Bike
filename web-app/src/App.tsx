import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { Route, Routes } from 'react-router-dom';
import { KeyStateProvider } from './context/KeyStateContext'; // KeyStateProvider のインポート
import theme from './theme';
import Map from './react/Map';
import Top from './react/Top';
import Proof from './react/Proof';
import './App.css';
import NotFound from './react/NotFound';

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <KeyStateProvider> {/* KeyStateProvider でラップ */}
        <Routes>
          <Route path="/" element={<Top />} />
          <Route path="/map" element={<Map />} />
          <Route path="*" element={<NotFound />} />
          <Route path="/proof" element={<Proof/>} />
        </Routes>
      </KeyStateProvider>
    </ThemeProvider>
  );
};

export default App;

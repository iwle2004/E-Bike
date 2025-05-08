import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { DocumentProvider } from './context/DocumentContext';
import { KeyStateProvider } from './context/KeyStateContext'; // KeyStateProvider のインポート
import CssBaseline from '@mui/material/CssBaseline';

// 'root' ID を持つ DOM 要素を取得
const root = document.getElementById('root')!;

// React アプリケーションを 'root' 要素にレンダリング
createRoot(root).render(
  <React.StrictMode>
    <CssBaseline />
    <BrowserRouter>
      <DocumentProvider>
        <KeyStateProvider> {/* KeyStateProvider を追加 */}
          <App />
        </KeyStateProvider>
      </DocumentProvider>
    </BrowserRouter>
  </React.StrictMode>
);

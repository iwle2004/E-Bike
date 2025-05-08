// src/context/KeyStateContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface KeyStateContextType {
  keyState: boolean | null;
  setKeyState: (keyState: boolean | null) => void; // 追加
}

const KeyStateContext = createContext<KeyStateContextType | undefined>(undefined);

export const KeyStateProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [keyState, setKeyState] = useState<boolean | null>(null);

  return (
    <KeyStateContext.Provider value={{ keyState, setKeyState }}>
      {children}
    </KeyStateContext.Provider>
  );
};

export const useKeyStateContext = () => {
  const context = useContext(KeyStateContext);
  if (!context) {
    throw new Error('useKeyStateContext must be used within a KeyStateProvider');
  }
  return context;
};

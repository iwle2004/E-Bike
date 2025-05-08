import React, { createContext, useContext, useState, ReactNode } from 'react';

interface DocumentContextType {
  selectedDocumentId: string;
  setSelectedDocumentId: (id: string) => void;
}

const DocumentContext = createContext<DocumentContextType | undefined>(undefined);

export const DocumentProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedDocumentId, setSelectedDocumentId] = useState<string>('');

  return (
    <DocumentContext.Provider value={{ selectedDocumentId, setSelectedDocumentId }}>
      {children}
    </DocumentContext.Provider>
  );
};

export const useDocumentContext = () => {
  const context = useContext(DocumentContext);
  if (!context) {
    throw new Error('useDocumentContext must be used within a DocumentProvider');
  }
  return context;
};

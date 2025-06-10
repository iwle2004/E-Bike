import React, { useState } from 'react';
import { doc, updateDoc, serverTimestamp } from 'firebase/firestore';
import db from '../firebase';
import { Box, Button, MenuItem, Select, TextField, Typography } from '@mui/material';
import { useDocumentContext } from '../context/DocumentContext';

const UpdateFirestoreDocument: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [error, setError] = useState('');
  const { selectedDocumentId, setSelectedDocumentId } = useDocumentContext();

  const documentOptions = [
    { id: 'higashiMaizuruSta', name: '東舞鶴駅' },
    { id: 'nitMaizuruCollege', name: '舞鶴高専' },
  ];

  const handleUpdate = async () => {
    // 入力値が整数かどうかをチェック
    const numericValue = parseInt(inputText, 10);
    if (isNaN(numericValue) || numericValue.toString() !== inputText) {
      setError('入力された値は整数ではありません。');
      return;
    }
    setError('');
    try {
      const docRef = doc(db, 'token', selectedDocumentId);
      await updateDoc(docRef, {
        inputToken: numericValue,
        timestamp: serverTimestamp()
      });
      console.log('Document updated successfully');
      setInputText('');
      // setSelectedDocumentId(''); // この行を削除またはコメントアウトして選択肢をリセットしない
    } catch (error) {
      console.error('Error updating document: ', error);
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" p={2}>
      <Select
        value={selectedDocumentId}
        onChange={(e) => setSelectedDocumentId(e.target.value)}
        displayEmpty
        variant="outlined"
        fullWidth
        sx={{ marginBottom: 2 }}
      >
        <MenuItem value="">
          <em>場所を選択</em>
        </MenuItem>
        {documentOptions.map((option) => (
          <MenuItem key={option.id} value={option.id}>
            {option.name}
          </MenuItem>
        ))}
      </Select>

      <TextField
        type="text" // 認証番号が整数であることを考慮して、type="text"に変更
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="認証番号"
        variant="outlined"
        fullWidth
        sx={{ marginBottom: 2 }}
      />

      <Button
        variant="contained"
        color="primary"
        onClick={handleUpdate}
        disabled={!selectedDocumentId || !inputText}
        fullWidth
        sx={{ marginBottom: 2 }}
      >
        送信
      </Button>

      {error && <Typography color="error">{error}</Typography>}
    </Box>
  );
};

export default UpdateFirestoreDocument;

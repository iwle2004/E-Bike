import React, { useState } from 'react';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import db from '../firebase';

const AddToFirestore: React.FC = () => {
  const [inputText, setInputText] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (inputText.trim() !== '') {
      try {
        const docRef = await addDoc(collection(db, 'posts'), {
          text: inputText,
          timestamp: serverTimestamp()
        });
        console.log('Document written with ID: ', docRef.id);
        setInputText('');
      } catch (error) {
        console.error('Error adding document: ', error);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter text"
      />
      <button type="submit">Add to Firestore</button>
    </form>
  );
};

export default AddToFirestore;

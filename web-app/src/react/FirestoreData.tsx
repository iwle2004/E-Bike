import React, { useEffect } from 'react';
import { doc, onSnapshot } from 'firebase/firestore';
import { useDocumentContext } from '../context/DocumentContext'; // DocumentContext をインポート
import { useKeyStateContext } from '../context/KeyStateContext'; // KeyStateContext をインポート
import db from '../firebase';

interface FirestoreDocData {
  keyState: boolean | null; // keyState フィールドの型を指定
}

const FirestoreData: React.FC = () => {
  const { selectedDocumentId } = useDocumentContext(); // useDocumentContext を使用
  const { setKeyState } = useKeyStateContext(); // useKeyStateContext を使用

  useEffect(() => {
    if (!selectedDocumentId) {
      return;
    }

    const docRef = doc(db, 'token', selectedDocumentId);

    // Firestore の onSnapshot メソッドを使用してデータの変更を監視
    const unsubscribe = onSnapshot(docRef, (docSnap) => {
      if (docSnap.exists()) {
        const docData = docSnap.data() as FirestoreDocData; // 型を指定
        setKeyState(docData.keyState); // KeyStateContext を更新
      } else {
        console.error('No such document!');
        setKeyState(null); // ドキュメントが存在しない場合の処理
      }
    }, (error) => {
      console.error('Error fetching document: ', error);
      setKeyState(null); // エラー処理
    });

    // クリーンアップ
    return () => unsubscribe();
  }, [selectedDocumentId, setKeyState]);

  return null; // 何も表示しない
};

export default FirestoreData;

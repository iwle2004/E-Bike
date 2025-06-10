import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAYJS8J_F2CXlno1y66RUy2Cd0EYhCM6ng",
  authDomain: "e-bike-maizuru.firebaseapp.com",
  projectId: "e-bike-maizuru",
  storageBucket: "e-bike-maizuru.firebasestorage.app",
  messagingSenderId: "158817887274",
  appId: "1:158817887274:web:0017501d8a752e697c0f53",
  measurementId: "G-SF85N57JZF"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app); 
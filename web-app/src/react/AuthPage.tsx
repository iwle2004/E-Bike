import React, { useState, FormEvent } from "react";
import "./AuthPage.css";
import { initializeApp } from "firebase/app";
import { useNavigate } from 'react-router-dom';
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAYJS8J_F2CXlno1y66RUy2Cd0EYhCM6ng",
  authDomain: "e-bike-maizuru.firebaseapp.com",
  projectId: "e-bike-maizuru",
  storageBucket: "e-bike-maizuru.firebasestorage.app",
  messagingSenderId: "158817887274",
  appId: "1:158817887274:web:0017501d8a752e697c0f53",
  measurementId: "G-SF85N57JZF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const AuthPage: React.FC = () => {
  const navigate = useNavigate();
  try {
    return (
      <div>Auth Page loaded</div> // Simplify for test
    );
  } catch (err) {
    console.error("Render error:", err);
    return <div>Error rendering AuthPage</div>;
  }
};

export default AuthPage;
// const AuthPage: React.FC = () => {
  // const [email, setEmail] = useState<string>("");
  // const [password, setPassword] = useState<string>("");
  // const [error, setError] = useState<string>("");
  // const [mode, setMode] = useState<"login" | "signup">("login");

  // const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   try {
  //     await signInWithEmailAndPassword(auth, email, password);
  //     alert("Logged in successfully");
  //   } catch (err: any) {
  //     setError(err.message);
  //   }
  // };

  // const handleSignup = async (e: FormEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   try {
  //     await createUserWithEmailAndPassword(auth, email, password);
  //     alert("Account created successfully");
  //   } catch (err: any) {
  //     setError(err.message);
  //   }
  // };

  // return (
    // <div className="auth-container">
    //   <div className="auth-card">
    //     <h2 className="auth-title">E-Bike Auth</h2>
    //     <div className="auth-tabs">
    //       <button className={mode === "login" ? "active" : ""} onClick={() => setMode("login")}>Login</button>
    //       <button className={mode === "signup" ? "active" : ""} onClick={() => setMode("signup")}>Signup</button>
    //     </div>
    //     <form onSubmit={mode === "login" ? handleLogin : handleSignup} className="auth-form">
    //       <label htmlFor="email">Email</label>
    //       <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />

    //       <label htmlFor="password">Password</label>
    //       <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />

    //       {error && <p className="error-text">{error}</p>}

    //       <button type="submit" className="auth-button">{mode === "login" ? "Log In" : "Sign Up"}</button>
    //     </form>
    //   </div>
    // </div>
    // <div>PISDAs</div>
  // );
// }
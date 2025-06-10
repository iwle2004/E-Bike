import { useState } from 'react';
import "./LoginPage.css";
function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const handleLogin = () => {
      if (email && password) {
        window.location.href = '/home';
      }
    };
  
    return (
      <div className="login-container">
        <div className="login-box">
          <h2 className="login-title">Login</h2>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
          />
          <button onClick={handleLogin} className="login-button">Login</button>
        </div>
      </div>
   );
}

export default LoginPage;
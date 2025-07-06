import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Rent.css';

function Rent() {
    const [file, setFile] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = () => {
        if (file) {
            alert('Photo submitted! Thank you.');
            setFile(null);
        }
    };

    const handleBack = () => {
        navigate('/'); // adjust if your main page route differs
    };

    return (
        <div className="photo-submit-container">
            <h2 className="photo-submit-title">ArUcoマーカーを撮影してください</h2>
            <input 
                type="file" 
                accept="image/*"
                onChange={(e) => setFile(e.target.files[0])} 
                className="photo-input" 
            />
            <br />
            <div className="example-box">
                <p className="example-title">撮影例</p>
                <img
                    src="./satsuei.jpg"
                    alt="撮影例"
                    className="example-image"
                />
            </div>
            <button onClick={handleSubmit} className="photo-button">SUBMIT</button>
        </div>
    );
}

export default Rent;

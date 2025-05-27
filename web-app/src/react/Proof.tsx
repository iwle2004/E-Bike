import React, { useState } from 'react';
import './Proof.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Proof: React.FC = () => {
    const [image, setImage] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setImage(file);
            setPreview(URL.createObjectURL(file));
        }
    };

  const handleSubmit = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await axios.post("/api/verify-dropoff", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { properly_parked, reason } = response.data;

      if (properly_parked) {
        alert("✅ Scooter drop-off confirmed. Thank you!");
        navigate("/ride-summary");
      } else {
        alert(`❌ Drop-off invalid: ${reason}. Please re-park and try again.`);
      }
    } catch (err) {
      console.error(err);
      alert("Error verifying image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="card">
        <h1 className="title">📍 Confirm Drop-off Location</h1>
        <p className="description">
          Please upload a photo of your parked scooter. Make sure it’s in a designated area and not blocking sidewalks or doors.
        </p>

        {preview && <img src={preview} alt="Preview" className="preview" />}

        <input
          type="file"
          accept="image/*"
          capture="environment"
          className="file-input"
            onChange={handleImageChange}
        />

        <button
          onClick={handleSubmit}
          disabled={loading || !image}
          className="submit-button"
        >
          {loading ? "Verifying..." : "Submit Photo"}
        </button>

        <button
          onClick={() => navigate("/")}
          className="back-button"
        >
          Go Back
        </button>
      </div>
    </div>
  );
  };
  
  export default Proof;
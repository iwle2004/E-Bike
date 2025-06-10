
import { useState } from 'react';

function PhotoSubmitPage() {
    const [file, setFile] = useState(null);
  
    const handleSubmit = () => {
      if (file) {
        alert('Photo submitted! Thank you.');
        setFile(null);
      }
    };
  
    return (
      <div className="photo-submit-container">
        <h2 className="photo-submit-title">Submit a Photo</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} className="photo-input" />
        <br />
        <button onClick={handleSubmit} className="photo-button">Submit Photo</button>
      </div>
    );
  }

  export default PhotoSubmitPage;
import { useState } from 'react';
import './PhotoSubmitPage.css'
import {useNavigate} from 'react-router-dom';

function PhotoSubmitPage() {
    const [file, setFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        if (selectedFile) {
            setPreviewUrl(URL.createObjectURL(selectedFile));
        } else {
            setPreviewUrl(null);
        }
    };

    const handleSubmit = () => {
        if (file) {
            alert('Photo submitted! Thank you.');
            navigate("/home");
            setFile(null);
            setPreviewUrl(null);
        }
    };

    return (
      <div className="photo-submit-container">
          <h2 className="photo-submit-title">Submit a Photo</h2>
          <input 
              type="file" 
              accept="image/*"
              onChange={handleFileChange} 
              className="photo-input" 
          />
          {previewUrl && (
              <div className="preview-container">
                  <p>Preview:</p>
                  <img 
                      src={previewUrl} 
                      alt="Preview" 
                      className="photo-preview" 
                  />
              </div>
          )}
  
          {/* 撮影例 box below */}
<div className="example-box">
    <p className="example-title">撮影例</p>
    <div className="example-images-container">
        <img
            src="./satsuei.jpg"
            alt="撮影例1"
            className="example-image"
        />
        <img
            src="./satsuei.jpg"
            alt="撮影例2"
            className="example-image"
        />
        <img
            src="./satsuei.jpg"
            alt="撮影例3"
            className="example-image"
        />
    </div>
</div>

  
          <br />
          <button onClick={handleSubmit} className="photo-button">Submit Photo</button>
      </div>
  );
  
}

export default PhotoSubmitPage;

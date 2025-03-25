import React, { useState } from 'react';

const DiagnosisDynamic = () => {
  const [modelFile, setModelFile] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  const handleModelChange = (e) => {
    setModelFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleImageChange = (e) => {
    setImageFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleDiagnosis = async () => {
    if (!modelFile || !imageFile) {
      alert("Vui lòng chọn cả file model và file ảnh.");
      return;
    }
    const formData = new FormData();
    formData.append('model_file', modelFile);
    formData.append('image_file', imageFile);

    try {
      const response = await fetch('http://localhost:912/api/diagnosis/pretrained', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h2>Dynamic Diagnosis (Upload Model & Image)</h2>
      <div>
        <label>Chọn file model (.h5): </label>
        <input type="file" accept=".h5" onChange={handleModelChange} />
      </div>
      <div style={{ marginTop: '10px' }}>
        <label>Chọn file ảnh: </label>
        <input type="file" accept="image/*" onChange={handleImageChange} />
      </div>
      <button onClick={handleDiagnosis} style={{ marginTop: '20px', padding: '10px 20px' }}>
        Dự đoán
      </button>
      {error && <div style={{ color: 'red', marginTop: '10px' }}>Error: {error}</div>}
      {result && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
          <p><strong>Kết quả:</strong> {result.diagnosis}</p>
          <p><strong>Độ tự tin:</strong> {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
};

export default DiagnosisDynamic;

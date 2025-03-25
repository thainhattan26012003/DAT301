// frontend/src/Home.js
import React, { useState } from 'react';
import Chatbot from '../components/Chatbot';

const Home = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [file, setFile] = useState(null);
  const [diagnosisResult, setDiagnosisResult] = useState(null);
  const token = localStorage.getItem('token');

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const imageUrl = URL.createObjectURL(selectedFile);
      setUploadedImage(imageUrl);
      setFile(selectedFile);
      // Reset diagnosis result khi chọn file mới
      setDiagnosisResult(null);
    }
  };

  const handleDiagnosis = async () => {
    if (!file) {
      alert("Vui lòng chọn ảnh.");
      return;
    }
    const formData = new FormData();
    formData.append('image_file', file);
    try {
      const response = await fetch('http://localhost:912/api/diagnosis/pretrained', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData,
      });
      const data = await response.json();
      setDiagnosisResult(data);
    } catch (err) {
      console.error(err);
      alert("Có lỗi xảy ra khi chẩn đoán.");
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Doctor AI - Chẩn đoán & Hỏi đáp</h1>
      </header>
      <div style={styles.content}>
        <div style={styles.leftPanel}>
          <div style={styles.uploadSection}>
            <h2 style={styles.sectionTitle}>Upload Ảnh</h2>
            <input type="file" accept="image/*" onChange={handleImageChange} />
            <button onClick={handleDiagnosis} style={styles.diagnosisButton}>Chẩn đoán</button>
          </div>
          <div style={styles.imageViewer}>
            {uploadedImage ? (
              <img src={uploadedImage} alt="Uploaded" style={{ maxWidth: '100%', maxHeight: '100%' }} />
            ) : (
              <p>Chưa có ảnh nào được tải lên</p>
            )}
          </div>
          {diagnosisResult && (
            <div style={styles.result}>
              <p><strong>Kết quả dự đoán:</strong> {diagnosisResult.predicted_label}</p>
              <p><strong>Độ tự tin:</strong> {(diagnosisResult.confidence * 100).toFixed(2)}%</p>
            </div>
          )}
        </div>
        <div style={styles.rightPanel}>
          <h2 style={styles.sectionTitle}>Chat Hỏi Đáp</h2>
          {/* Truyền diagnosisResult (chuyển thành chuỗi JSON) làm prop cho Chatbot */}
          <Chatbot diagnosis={diagnosisResult ? JSON.stringify(diagnosisResult) : ""} />
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: { height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: 'Arial, sans-serif' },
  header: { background: '#9b59b6', padding: '20px', textAlign: 'center', color: '#fff' },
  title: { margin: 0, fontSize: '28px' },
  content: { flex: 1, display: 'flex', overflow: 'hidden' },
  leftPanel: { flex: 1, padding: '20px', borderRight: '1px solid #ccc', overflowY: 'auto' },
  rightPanel: { flex: 1, padding: '20px', display: 'flex', flexDirection: 'column', overflow: 'hidden' },
  uploadSection: { marginBottom: '20px' },
  sectionTitle: { fontSize: '20px', marginBottom: '15px', color: '#333' },
  imageViewer: { display: 'flex', justifyContent: 'center', alignItems: 'center', border: '1px solid #ccc', height: '400px' },
  diagnosisButton: { marginTop: '10px', padding: '10px 20px', backgroundColor: '#9b59b6', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  result: { marginTop: '20px', padding: '10px', border: '1px solid #ccc' },
};

export default Home;

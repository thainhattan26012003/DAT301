// frontend/src/components/UserImages.js
import React, { useState, useEffect } from 'react';

const UserImages = () => {
  const [images, setImages] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetch('http://localhost:912/api/diagnosis/images', {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then(res => res.json())
      .then(data => setImages(data.images))
      .catch(err => console.error(err));
  }, [token]);

  return (
    <div>
      <h2>Ảnh khám trước của bạn</h2>
      {images.length > 0 ? (
        images.map((img, idx) => (
          <div key={idx} style={{ marginBottom: '10px' }}>
            <img src={img.file_url} alt={`Ảnh ${idx + 1}`} style={{ maxWidth: '100%' }} />
            <p>Thời gian: {new Date(img.timestamp).toLocaleString()}</p>
          </div>
        ))
      ) : (
        <p>Chưa có ảnh nào được lưu trữ.</p>
      )}
    </div>
  );
};

export default UserImages;

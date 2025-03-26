// src/components/ImageHistory.js
import React, { useState, useEffect } from 'react';

export default function ImageHistory() {
  const [images, setImages] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetch('http://localhost:912/images/my-images', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setImages(data.data);
        }
      })
      .catch(err => console.error(err));
  }, [token]);

  return (
    <div>
      <h3>Ảnh Đã Upload</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {images.map(img => (
          <div key={img._id} style={{ margin: 10 }}>
            <img 
              src={img.image_url} 
              alt="user_img" 
              style={{ width: '200px', height: 'auto' }} 
            />
            {/* Nếu có chẩn đoán cũ thì hiển thị ở đây */}
          </div>
        ))}
      </div>
    </div>
  );
}

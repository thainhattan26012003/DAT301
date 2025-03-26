// src/components/UploadImage.js
import React, { useState } from 'react';

export default function UploadImage() {
  const [file, setFile] = useState(null);
  const token = localStorage.getItem('token');

  const handleSelectFile = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('http://localhost:912/api/images/upload', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });
      const data = await res.json();
      if (data.success) {
        alert("Upload thành công: " + data.image_url);
      } else {
        alert("Upload thất bại");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h3>Upload Ảnh</h3>
      <input type="file" accept="image/*" onChange={handleSelectFile} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

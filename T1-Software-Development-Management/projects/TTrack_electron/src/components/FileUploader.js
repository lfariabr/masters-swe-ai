/**
 * FileUploader Component
 * Handles file upload UI and functionality
 */
import React from 'react';

const FileUploader = ({ type, onFileUpload, label, icon }) => {
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file, type);
    }
  };

  return (
    <label className="upload-btn">
      {icon} {label}
      <input
        type="file"
        accept=".xlsx, .xls"
        hidden
        onChange={handleChange}
      />
    </label>
  );
};

export default FileUploader;

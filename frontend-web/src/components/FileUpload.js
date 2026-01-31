/**
 * FileUpload Component
 *
 * Handles CSV file selection via:
 * - Click to browse
 * - Drag and drop
 */
import React, { useState, useRef } from "react";

function FileUpload({ onUpload, loading }) {
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);

  /**
   * Handle file selection from input
   */
  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  /**
   * Handle drag events
   */
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".csv")) {
      onUpload(file);
    }
  };

  /**
   * Trigger file input click
   */
  const handleClick = () => {
    if (!loading) {
      fileInputRef.current.click();
    }
  };

  return (
    <div
      className={`file-upload ${dragging ? "dragging" : ""}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <input
        type="file"
        ref={fileInputRef}
        accept=".csv"
        onChange={handleFileSelect}
      />
      <p>Drop your CSV file here, or</p>
      <button className="browse-btn" disabled={loading}>
        {loading ? "Uploading..." : "Choose File"}
      </button>
    </div>
  );
}

export default FileUpload;

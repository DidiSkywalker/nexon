import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadMessage("Please select a file before uploading.");
      return;
    }

    // Simulated upload process (replace with actual upload logic if needed)
    try {
      const formData = new FormData();
      formData.append("file", file);

      // Example API call to upload the file (uncomment and adjust URL when needed)
      // await axios.post('your-api-endpoint', formData);

      setUploadMessage("File uploaded successfully!");
    } catch (error) {
      setUploadMessage("Failed to upload the file. Please try again.");
    }
  };

  return (
    <div style={styles.container}>
      {/* Upload Card */}
      <div style={styles.uploadCard}>
        <h1 style={styles.title}>Upload Your ONNX Model</h1>
        <p style={styles.description}>
          Select your ONNX model file to upload and deploy it on the platform.
        </p>

        {/* File Input */}
        <input
          type="file"
          onChange={handleFileChange}
          style={styles.fileInput}
        />

        {/* Upload Button */}
        <button onClick={handleUpload} style={styles.uploadButton}>
          Upload
        </button>

        {/* Upload Status Message */}
        {uploadMessage && (
          <p style={styles.uploadMessage}>{uploadMessage}</p>
        )}
      </div>
    </div>
  );
};

export default Upload;

const styles = {
  container: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#1f1f2e",
    fontFamily: "'Roboto', sans-serif",
    color: "#fff",
  },
  uploadCard: {
    backgroundColor: "#2a2a3c",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
    textAlign: "center",
    width: "400px",
  },
  title: {
    fontSize: "24px",
    fontWeight: "bold",
    marginBottom: "15px",
    color: "#f9a825",
  },
  description: {
    fontSize: "16px",
    marginBottom: "20px",
    color: "#c2c2c2",
  },
  fileInput: {
    marginBottom: "20px",
    padding: "10px",
    fontSize: "14px",
    color: "#fff",
    backgroundColor: "#1f1f2e",
    border: "1px solid #6a11cb",
    borderRadius: "8px",
    outline: "none",
    cursor: "pointer",
  },
  uploadButton: {
    backgroundColor: "#2575fc",
    color: "#fff",
    border: "none",
    padding: "10px 20px",
    fontSize: "16px",
    fontWeight: "bold",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s ease",
  },
  uploadButtonHover: {
    backgroundColor: "#6a11cb",
  },
  uploadMessage: {
    marginTop: "20px",
    fontSize: "14px",
    color: "#6a11cb",
  },
};

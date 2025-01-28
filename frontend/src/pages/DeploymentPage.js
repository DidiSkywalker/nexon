import React, { useState } from "react";

const Deploy = () => {
  const [selectedModel, setSelectedModel] = useState("");
  const [file, setFile] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");

  const handleModelChange = (event) => {
    setSelectedModel(event.target.value);
    setFile(null); // Clear file selection if a model is selected
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setSelectedModel(""); // Clear model selection if a file is uploaded
  };

  const handleDeploy = () => {
    if (!selectedModel && !file) {
      setStatusMessage("Please select a model or upload a file before deploying.");
      return;
    }

    if (file) {
      setStatusMessage(`File "${file.name}" uploaded and deployed successfully!`);
    } else {
      setStatusMessage(`Model "${selectedModel}" deployed successfully!`);
    }
  };

  return (
    <div style={styles.container}>
      {/* Deployment Card */}
      <div style={styles.deployCard}>
        <h1 style={styles.title}>Deploy Your Model</h1>
        <p style={styles.description}>
          Select an existing model to deploy.
        </p>

        {/* Dropdown for Model Selection */}
        <select
          value={selectedModel}
          onChange={handleModelChange}
          style={styles.dropdown}
        >
          <option value="">-- Select a Model --</option>
          <option value="DummyFile">DummyFile</option>
        </select>

        <p style={styles.orText}>OR</p>

        {/* File Upload Section */}
        <div style={styles.fileUpload}>
          <label style={styles.fileLabel} htmlFor="fileInput">
            Choose a new File
          </label>
          <input
            type="file"
            id="fileInput"
            onChange={handleFileChange}
            style={styles.fileInput}
          />
        </div>

        {/* Deploy Button */}
        <button onClick={handleDeploy} style={styles.deployButton}>
          Deploy
        </button>

        {/* Status Message */}
        {statusMessage && <p style={styles.statusMessage}>{statusMessage}</p>}
      </div>
    </div>
  );
};

export default Deploy;

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
  deployCard: {
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
  dropdown: {
    width: "100%",
    padding: "10px",
    fontSize: "14px",
    color: "#fff",
    backgroundColor: "#1f1f2e",
    border: "1px solid #6a11cb",
    borderRadius: "8px",
    marginBottom: "20px",
    outline: "none",
    cursor: "pointer",
  },
  orText: {
    fontSize: "16px",
    fontWeight: "bold",
    margin: "20px 0",
    color: "#c2c2c2",
  },
  fileUpload: {
    marginBottom: "20px",
  },
  fileLabel: {
    display: "block",
    marginBottom: "10px",
    fontSize: "14px",
    color: "#c2c2c2",
  },
  fileInput: {
    width: "100%",
    padding: "10px",
    fontSize: "14px",
    color: "#fff",
    backgroundColor: "#1f1f2e",
    border: "1px solid #6a11cb",
    borderRadius: "8px",
    outline: "none",
    cursor: "pointer",
  },
  deployButton: {
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
  statusMessage: {
    marginTop: "20px",
    fontSize: "14px",
    color: "#6a11cb",
  },
};

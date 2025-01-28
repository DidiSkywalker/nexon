import React, { useState } from "react";
import axios from "axios";

const Inference = () => {
  const [file, setFile] = useState(null);
  const [inputs, setInputs] = useState("");
  const [results, setResults] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleInputChange = (event) => {
    setInputs(event.target.value);
  };

  const handleUploadModel = async () => {
    if (!file) {
      setStatusMessage("Please upload an ONNX model file.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post("http://127.0.0.1:8000/inference/upload-model/", formData);

      setStatusMessage(response.data.message);
    } catch (error) {
      setStatusMessage("Error uploading model: " + error.response?.data?.detail || error.message);
    }
  };

  const handleRunInference = async () => {
    if (!inputs) {
      setStatusMessage("Please provide input data for inference.");
      return;
    }

    try {
      const inputData = JSON.parse(inputs);

      const response = await axios.post("http://127.0.0.1:8000/inference/infer/", { inputs: inputData });

      setResults(response.data.results);
      setStatusMessage("Inference completed successfully!");
    } catch (error) {
      setStatusMessage("Error during inference: " + error.response?.data?.detail || error.message);
    }
  };

  return (
    <div style={styles.container}>
      {/* Input Section */}
      <div style={styles.inputSection}>
        <h1 style={styles.title}>Run Inference</h1>
        <p style={styles.description}>
          Upload your ONNX model, provide input data, and view the results.
        </p>

        {/* Upload Model */}
        <div style={styles.section}>
          <label style={styles.label}>Upload ONNX Model:</label>
          <input type="file" onChange={handleFileChange} style={styles.fileInput} />
          <button onClick={handleUploadModel} style={styles.button}>
            Upload Model
          </button>
        </div>

        {/* Input Data */}
        <div style={styles.section}>
          <label style={styles.label}>Input Data (JSON format):</label>
          <textarea
            value={inputs}
            onChange={handleInputChange}
            style={styles.textarea}
            placeholder='e.g., [[1.0, 2.0, 3.0]]'
          />
        </div>

        {/* Run Inference */}
        <button onClick={handleRunInference} style={styles.button}>
          Run Inference
        </button>

        {/* Status Message */}
        {statusMessage && <p style={styles.statusMessage}>{statusMessage}</p>}
      </div>

      {/* Results Section */}
      <div style={styles.resultsSection}>
        <h2 style={styles.resultsTitle}>Results</h2>
        <div style={styles.resultsBox}>
          {results ? (
            <pre style={styles.resultsContent}>
              {JSON.stringify(results, null, 2)}
            </pre>
          ) : (
            <p style={styles.placeholderText}>Results will appear here.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Inference;

const styles = {
  container: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    height: "100vh",
    backgroundColor: "#1f1f2e",
    fontFamily: "'Roboto', sans-serif",
    color: "#fff",
  },
  inputSection: {
    flex: 1,
    padding: "30px",
    backgroundColor: "#2a2a3c",
    borderRadius: "12px",
    margin: "20px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
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
  section: {
    marginBottom: "20px",
  },
  label: {
    fontSize: "14px",
    color: "#c2c2c2",
    marginBottom: "10px",
    display: "block",
  },
  fileInput: {
    width: "100%",
    padding: "10px",
    fontSize: "14px",
    color: "#fff",
    backgroundColor: "#1f1f2e",
    border: "1px solid #6a11cb",
    borderRadius: "8px",
    marginBottom: "10px",
    outline: "none",
    cursor: "pointer",
  },
  textarea: {
    width: "100%",
    padding: "10px",
    fontSize: "14px",
    color: "#fff",
    backgroundColor: "#1f1f2e",
    border: "1px solid #6a11cb",
    borderRadius: "8px",
    outline: "none",
    height: "100px",
  },
  button: {
    backgroundColor: "#2575fc",
    color: "#fff",
    border: "none",
    padding: "10px 20px",
    fontSize: "16px",
    fontWeight: "bold",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s ease",
    width: "100%",
    marginTop: "10px",
  },
  statusMessage: {
    marginTop: "20px",
    fontSize: "14px",
    color: "#6a11cb",
  },
  resultsSection: {
    flex: 1,
    padding: "30px",
    margin: "20px",
    backgroundColor: "#2a2a3c",
    borderRadius: "12px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
    overflow: "hidden",
  },
  resultsTitle: {
    fontSize: "20px",
    fontWeight: "bold",
    marginBottom: "15px",
    color: "#f9a825",
  },
  resultsBox: {
    backgroundColor: "#1f1f2e",
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #6a11cb",
    maxHeight: "80vh",
    overflow: "auto",
  },
  resultsContent: {
    fontSize: "14px",
    color: "#fff",
    whiteSpace: "pre-wrap",
  },
  placeholderText: {
    fontSize: "14px",
    color: "#c2c2c2",
  },
};

import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const ModelOverview = () => {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null); 
  const navigate = useNavigate();

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/allModels")
      .then(response => {
        setModels(response.data);
      })
      .catch(error => console.error("Error fetching models:", error));
  }, []);

  const goBack = () => navigate(-1);
  const navToHomePage = () => navigate('/home');
  const navToInferencePage = (modelName) => navigate(`/inference?model=${modelName}`);

  return (
    <div style={styles.container}>
      <div style={styles.backButtonContainer}>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
        <i className="material-icons" style={styles.homeIcon} onClick={navToHomePage}>home</i>
        <button onClick={goBack} style={styles.backButton}>← Back</button>
      </div>
      <h1 style={styles.title}>Model Overview</h1>

      {models.length === 0  ? (
        <p style={styles.noModels}>No models uploaded yet.</p>
      ) : (
        <div style={styles.modelGrid}>
          {models.map((model, index) => (
            <div key={index} style={styles.modelCard} className="model-card">
              <h3 style={styles.modelName}>{model.name}</h3>
              <p>📅 Uploaded: {model.upload || "Unknown"}</p>
              <p>📦 Size: {model.size || "N/A"}</p>
              {model.status === "Deployed" ? (<div><p>⚡ Status: Deployed</p> <button style={styles.button} onClick={() => setSelectedModel(model)}>View Details</button> </div>):
              ( <div><p>⚡ Status: Pending</p> <button style={styles.button} onClick={() => navigate(`/deploy?model=${model.name}`)}>Deploy</button> </div>) }
            </div>
          ))} 
        </div>
      )}

      {/* ✅ Modal for Model Details */}
      {selectedModel && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalContent}>
            <h2>Model Details</h2>
            <p><strong>Name:</strong> {selectedModel.name}</p>
            <p><strong>ID:</strong> {selectedModel._id}</p>
            <p><strong>Version:</strong> 1.0</p>
            <p><strong>Deployed:</strong> {selectedModel.deploy}</p>
            <p><strong>REST API Endpoint:</strong></p>
            <p style={styles.apiBox}>http://127.0.0.1:8000/inference/infer/{selectedModel.name}</p>
            <button style={styles.inferenceButton} onClick={() => navToInferencePage(selectedModel.name)}>Go to Inference</button>
            <button style={styles.closeButton} onClick={() => setSelectedModel(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelOverview;

const styles = {
  container: {
    padding: "40px",
    backgroundColor: "#1f1f2e",
    color: "#fff",
    fontFamily: "'Roboto', sans-serif",
    minHeight: "100vh",
  },
  title: {
    fontSize: "28px",
    marginBottom: "20px",
    color: "#f9a825",
  },
  noModels: {
    textAlign: "center",
    fontSize: "18px",
    color: "#ccc",
  },
  modelGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, minmax(250px, 1fr))",
    gap: "20px",
  },
  modelCard: {
    backgroundColor: "#2a2a3c",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
    textAlign: "center",
  },
  modelName: {
    fontSize: "20px",
    marginBottom: "10px",
    color: "#f9a825",
  },
  button: {
    marginTop: "10px",
    padding: "10px",
    border: "none",
    backgroundColor: "#2575fc",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background 0.3s ease",
  },
  backButton: {
    position: "absolute",
    top: "20px",
    left: "20px",
    background: "transparent",
    boxShadow: "none",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
  },
  homeIcon: {
    position: "absolute",
    cursor: "pointer",
    top: "25px",
    right: "25px",
    fontSize: "200%",
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.7)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    backgroundColor: "#2a2a3c",
    padding: "20px",
    borderRadius: "10px",
    textAlign: "center",
    color: "#fff",
    width: "400px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
  },
  apiBox: {
    backgroundColor: "#1f1f2e",
    padding: "10px",
    borderRadius: "5px",
    wordBreak: "break-all",
    border: "1px solid #6a11cb",
  },
  inferenceButton: {
    backgroundColor: "#2575fc",
    color: "#fff",
    padding: "10px 15px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    fontSize: "16px",
    marginTop: "10px",
    marginRight: "10px",
  
  },
  closeButton: {
    backgroundColor: "#ff4d4d",
    color: "#fff",
    padding: "10px 15px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    fontSize: "16px",
    marginTop: "10px",
    marginLeft: "10px"
  },
  testGrid: {
    display: "grid",
    gridTemplateRows: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "20px",
  },
  testCard: {
    backgroundColor: "#2a2a3c",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
    textAlign: "left",
  },
  testSpan: {
    textAlign: "left",
  },
  testButton: {
    float: "right"
  }
};

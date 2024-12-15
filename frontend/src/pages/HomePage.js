import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  // Navigation handler
  const navigateTo = (path) => {
    navigate(path);
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.welcome}>Welcome, Hussein</h1>
      </header>
      <div style={styles.gridContainer}>
        <div style={styles.gridItem} onClick={() => navigateTo("/upload")}>
          <h2>Upload</h2>
          <p>Upload your ONNX models.</p>
        </div>
        <div style={styles.gridItem} onClick={() => navigateTo("/deploy")}>
          <h2>Deploy</h2>
          <p>Deploy ONNX models to production.</p>
        </div>
        <div style={styles.gridItem} onClick={() => navigateTo("/inference")}>
          <h2>Inference</h2>
          <p>Run inference on uploaded models.</p>
        </div>
        <div style={styles.gridItem} onClick={() => navigateTo("/metadata")}>
          <h2>Metadata</h2>
          <p>Manage model metadata.</p>
        </div>
        <div style={styles.gridItem} onClick={() => navigateTo("/history")}>
          <h2>History</h2>
          <p>View deployment and inference history.</p>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: "'Roboto', sans-serif",
    textAlign: "center",
    backgroundColor: "#f4f4f9",
    height: "100vh",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    padding: "20px",
    backgroundColor: "#2575fc",
    color: "#fff",
    textAlign: "left",
  },
  welcome: {
    margin: 0,
    fontSize: "24px",
  },
  gridContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
    gap: "20px",
    padding: "40px",
    margin: "auto",
    maxWidth: "1000px",
  },
  gridItem: {
    backgroundColor: "#2575fc",
    color: "#fff",
    borderRadius: "10px",
    padding: "20px",
    textAlign: "center",
    cursor: "pointer",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    transition: "transform 0.3s, box-shadow 0.3s",
  },
  gridItemHover: {
    transform: "scale(1.05)",
    boxShadow: "0 6px 12px rgba(0, 0, 0, 0.2)",
  },
  gridItemHeading: {
    fontSize: "20px",
    marginBottom: "10px",
  },
  gridItemDescription: {
    fontSize: "14px",
    color: "#ddd",
  },
};

export default Home;

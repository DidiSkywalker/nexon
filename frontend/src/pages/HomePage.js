import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  const [hoveredMenu, setHoveredMenu] = useState(null);

  const handleMouseEnter = (menuItem) => {
    setHoveredMenu(menuItem);
  };

  const handleMouseLeave = () => {
    setHoveredMenu(null);
  };

  const navToUploadPage = () => {
    navigate('/upload');
  };
  const navToDeployPage = () => {
    navigate('/deploy');
  };
  const navToInferencePage = () => {
    navigate('/inference');
  };
  const navToOverview = () => {
    navigate('/overview');
  };

  return (
    <div style={styles.container}>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>

      {/* Header Section */}
      <header style={styles.header}>
        <div style={styles.logo}>NEXON</div>
        <nav style={styles.nav}>
          {["Upload", "Deploy", "Inference", "Model Overview"].map((item, index) => (
            <span
              key={index}
              onClick={
                item === "Upload" ? navToUploadPage :
                item === "Deploy" ? navToDeployPage :
                item === "Inference" ? navToInferencePage :
                item === "Model Overview" ? navToOverview :
                undefined
              }
              style={{
                ...styles.menuButton,
                fontWeight: hoveredMenu === item ? "bold" : "normal",
              }}
              onMouseEnter={() => handleMouseEnter(item)}
              onMouseLeave={handleMouseLeave}
            >
              {item}
            </span>
          ))}
        </nav>
      </header>

      {/* Hero Section */}
      <section style={styles.hero}>
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>Seamless AI Model Deployment Made Easy</h1>
          <p style={styles.heroSubtitle}>
            Deploy, manage, and infer ONNX models with ease on a modern platform designed for efficiency and scale.
          </p>
          <button style={styles.heroButton} onClick={navToUploadPage}>
            Start by uploading models
          </button>
        </div>
      </section>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: "'Roboto', sans-serif",
    color: "#fff",
    backgroundColor: "#1f1f2e",
    margin: 0,
    padding: 0,
    height: "100vh",
  },
  header: {
    position: "relative", // Required for absolute positioning of the nav
    display: "flex",
    alignItems: "center",
    padding: "20px 50px",
    backgroundColor: "#1f1f2e",
  },
  logo: {
    fontSize: "32px",
    fontWeight: "bold",
    color: "#fff",
  },
  nav: {
    position: "absolute", // Position the nav absolutely
    left: "50%", // Move the nav to the horizontal center
    transform: "translateX(-50%)", // Adjust for the nav's own width
    display: "flex",
    gap: "20px",
  },
  welcomeText: {
    marginTop: "5px",
    fontSize: "16px",
    color: "#fff",
  },
  hero: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "80vh",
    backgroundImage: `url('https://via.placeholder.com/1920x1080')`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    textAlign: "center",
    marginTop: "-50px",
  },
  heroContent: {
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    padding: "40px",
    borderRadius: "15px",
    width: "80%",
    maxWidth: "800px",
  },
  heroTitle: {
    fontSize: "64px",
    fontWeight: "bold",
    marginBottom: "30px",
    color: "#f9a825",
  },
  heroSubtitle: {
    fontSize: "22px",
    marginBottom: "30px",
  },
  heroButton: {
    backgroundColor: "#2575fc",
    border: "none",
    color: "#fff",
    padding: "15px 40px",
    borderRadius: "10px",
    cursor: "pointer",
    fontSize: "20px",
    fontWeight: "bold",
    transition: "background-color 0.3s ease",
  },
  menuButton: {
    position: "relative",
    cursor: "pointer",
    transition: "font-weight 0.2s ease",
    fontSize: "22px"
  },
};

export default Home;
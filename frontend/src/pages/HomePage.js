import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const navToUploadPage = () => {
    navigate('/upload');
  };
  const navToDeployPage = () => {
    navigate('/deploy');
  };
  const navToInferencePage = () => {
    navigate('/inference');
  };
  return (
    <div style={styles.container}>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
      
      {/* Header Section */}
      <header style={styles.header}>
        <div style={styles.logo}>NEXON</div>
        <nav style={styles.nav}>
          <a href="#upload" style={styles.navLink} onClick={navToUploadPage}>Upload</a>
          <a href="#deploy" style={styles.navLink} onClick={navToDeployPage}>Deploy</a>
          <a href="#infer" style={styles.navLink} onClick={navToInferencePage}>Inference</a>
          <a href="#faq" style={styles.navLink}>Metadata Management</a>
          <a href="#contact" style={styles.navLink}>History</a>
        </nav>
        <div style={styles.profileContainer}>
          <i className="material-icons" style={styles.profile}>person</i>
          <span style={styles.welcomeText}>Welcome, User</span>
        </div>
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
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "20px 50px",
    backgroundColor: "#1f1f2e",
  },
  logo: {
    fontSize: "28px",
    fontWeight: "bold",
    color: "#fff",
  },
  nav: {
    display: "flex",
    gap: "20px",
  },
  navLink: {
    color: "#fff",
    textDecoration: "none",
    fontSize: "16px",
    transition: "color 0.3s ease",
  },
  profileContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  profile: {
    fontSize: "40px", // Enlarged the person icon
    color: "#fff",
    cursor: "pointer",
    transition: "color 0.3s ease",
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
    height: "80vh", // Reduced height to move it up
    backgroundImage: `url('https://via.placeholder.com/1920x1080')`, // Replace this with a suitable AI/cloud image
    backgroundSize: "cover",
    backgroundPosition: "center",
    textAlign: "center",
    marginTop: "-50px", // Added negative margin to move it closer to the header
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
};

export default Home;

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import background from "../img/AIBackground.jpg";

const Start = () => {
    const navigate = useNavigate();

    const navToHomePage = () => {
            navigate('/home');
    };

    return (
        <div style={styles.container}>
            <header style={{ opacity: 0 }}>Test</header>
            <div style={styles.welcomeText}>
                <h1 style={styles.title}>Welcome to NEXON</h1>
                <p style={styles.subtitle}>Deploy and manage your ONNX models with ease</p>
                    <button onClick={navToHomePage} style={styles.button}>Start Deploying!</button>
                </div>
            </div>
    );
};

const styles = {
    container: {
        backgroundImage: `url(${background})`,
        color: "#fff",
        backgroundColor: "#1f1f2e",
        margin: 0,
        padding: 0,
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    welcomeText: {
        textAlign: "center",
        backgroundColor: "rgba(31, 31, 46, 0.85)", // Semi-transparent background
        padding: "30px",
        borderRadius: "15px",
        width: "400px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
    },
    title: {
        fontSize: "36px",
        color: "white",
        marginBottom: "10px",
    },
    subtitle: {
        fontSize: "18px",
        color: "white",
        marginBottom: "20px",
    },
    form: {
        display: "flex",
        flexDirection: "column",
        gap: "15px",
    },
    label: {
        fontSize: "14px",
        color: "#ccc",
        textAlign: "left",
    },
    input: {
        flex: 1,
        padding: "10px",
        fontSize: "16px",
        borderRadius: "5px",
        border: "1px solid #6a11cb",
        outline: "none",
        transition: "border-color 0.3s ease",
    },
    passwordContainer: {
        display: "flex",
        alignItems: "center",
        position: "relative",
    },
    eyeIcon: {
        position: "absolute",
        right: "10px",
        cursor: "pointer",
        fontSize: "18px",
        color: "black",
        userSelect: "none",
    },
    button: {
        marginTop: "10px",
        padding: "20px",
        fontSize: "20px",
        fontWeight: "bold",
        backgroundColor: "#2575fc",
        color: "#fff",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
        transition: "background-color 0.3s ease",
    },
    error: {
        color: "#ff4d4d",
        fontSize: "14px",
        marginTop: "10px",
        textAlign: "left",
    },
};

export default Start;

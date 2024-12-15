import React from "react";
import { useNavigate } from "react-router-dom";


const Start = () => {
    const navigate = useNavigate();

    const navToDeployPage = () => {
        navigate('/home');
    }

    return (
        <div id="WelcomeText" style={{ textAlign: "center", marginTop: "7cm" }}>
            <h1 style={{ fontSize: "36px", color: "#333" }}>Welcome to NEXON</h1>
            <p style={{ fontSize: "18px", color: "#555" }}>Deploy and manage your ONNX models with ease</p>
            <button onClick={navToDeployPage}>Start Deploying!</button>
        </div>
    )
}

export default Start;
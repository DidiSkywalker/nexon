
# NEXON

The **ONNX Deployment Platform** NEXON is a web-based application that allows users to upload, deploy, and run inference on ONNX models easily. It provides a user-friendly interface for managing AI models and executing inference tasks.

## 🚀 Features
- Upload and deploy ONNX models.
- Perform inference with custom input data.
- View inference results in a results panel.
- Modern, responsive UI with an intuitive layout.

---

## 📦 Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/onnx-deployment-platform.git
cd onnx-deployment-platform
```
### **2. Set Up the Backend**
Navigate to the server directory and create a virtual environment:
```bash
cd server
python -m venv onnx_platform_env
source onnx_platform_env/bin/activate  # (Windows: onnx_platform_env\Scripts\activate)
```
Install dependencies: 
```bash
pip install -r requirements.txt
```
Run the FastAPI backend:
```bash
uvicorn main:app --reload
```
### **2. Set Up the Forntend**
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
npm start
```
## 🛠 Usage
## API Endpoints
## Troubleshooting


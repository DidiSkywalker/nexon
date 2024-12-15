import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };


  return (
    <div id="deploy">
      <h1>Upload ONNX Model</h1>
      <input type="file" onChange={handleFileChange} />
      <button>Upload</button>
    </div>
  );
};

export default Upload;

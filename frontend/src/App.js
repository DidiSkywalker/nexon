
import './styles/App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Start from "./pages/StartPage.js";
import Deploy from "./pages/DeploymentPage.js"
import Home from "./pages/HomePage.js"
import Upload from './pages/UploadPage.js';
import Inference from './pages/InferencePage.js';
import ModelOverview from './pages/ModelOverview.js';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Start/>}/>
        <Route path='/home' element={<Home/>}/>
        <Route path='/deploy' element={<Deploy/>}/>
        <Route path='/upload' element={<Upload/>}/>
        <Route path='/inference' element={<Inference/>}/>
        <Route path='/overview' element={<ModelOverview/>}/>
      </Routes>
    </Router>
  );
}

export default App;

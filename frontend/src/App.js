import logo from './logo.svg';
import './styles/App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Start from "./pages/StartPage.js";
import Deploy from "./pages/DeploymentPage.js"
import Home from "./pages/HomePage.js"

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Start/>}/>
        <Route path='/home' element={<Home/>}/>
        <Route path='/upload' element={<Deploy/>}/>
      </Routes>
    </Router>
  );
}

export default App;

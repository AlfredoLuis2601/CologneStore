import { CologneDetailsPage } from "./pages/CologneDetailsPage.jsx";
import Home from "./pages/Home.jsx"
import {Route,Routes} from "react-router"

function App() {
  return(
   <Routes>
    <Route path="/" element={<Home/>}></Route>
    <Route path="/colognedetails/:uid" element={<CologneDetailsPage/>}/>
   </Routes>
  );
}

export default App

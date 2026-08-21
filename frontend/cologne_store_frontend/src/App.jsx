import { CologneDetailsPage } from "./pages/CologneDetailsPage.jsx";
import Home from "./pages/Home.jsx"
import { LoginPage } from "./pages/LoginPage.jsx"
import {Navigate, Route,Routes} from "react-router"
import "./App.css"
import { SignUpPage } from "./pages/SignUp.jsx"
import { AuthLayout } from "./components/layout/AuthLayout.jsx";
import { RequestPasswordResetPage } from "./pages/PasswordResetMailPage.jsx";
import { VerifyMailProvider } from "./hooks/context.jsx";

function App() {
  return(
   <Routes>
    <Route path="/" element={<Home/>}></Route>
      <Route path="/auth" element={<AuthLayout/>}>
        <Route index element={<LoginPage/>}/>
        <Route path="register" element={<SignUpPage/>}/>
        <Route path="requestreset" element={<RequestPasswordResetPage/>}/>
      </Route>
    <Route path="/colognedetails/:uid" element={<CologneDetailsPage/>}/>
   </Routes>
  );
}

export default App

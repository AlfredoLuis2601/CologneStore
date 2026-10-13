import { CologneDetailsPage } from "./products/pages/CologneDetails.jsx";
import Home from "./products/pages/Home.jsx"
import { LoginPage } from "./auth/pages/LoginPage.jsx"
import { Route,Routes} from "react-router"
import "./App.css"
import { SignUpPage } from "./auth/pages/SignUp.jsx"
import { AuthLayout } from "./auth/components/AuthLayout.jsx";
import { RequestPasswordResetPage } from "./auth/pages/PasswordResetMail.jsx";
import { VerifyMailPage } from "./auth/pages/VerifyMail.jsx";
import { PasswordReset } from "./auth/pages/PasswordReset.jsx";
import { CheckoutPage } from "./checkout/pages/Checkout.jsx";
import { Orders } from "./checkout/pages/Orders.jsx";

function App() {
  return(
   <Routes>
    <Route path="/" element={<Home/>}></Route>
      <Route path="/auth" element={<AuthLayout/>}>
        <Route index element={<LoginPage/>}/>
        <Route path="register" element={<SignUpPage/>}/>
        <Route path="passwordreset/:key" element={<PasswordReset/>}/>
        <Route path="verifymail/:key" element={<VerifyMailPage/>}/>
        <Route path="requestreset" element={<RequestPasswordResetPage/>}/>
      </Route>
    <Route path="/colognedetails/:uid" element={<CologneDetailsPage/>}/>
    <Route path="/checkout" element={<CheckoutPage/>}/>
    <Route path="/orders" element={<Orders/>}/>
   </Routes>
  );
}

export default App

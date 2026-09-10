import { useState } from "react"
import { useUser } from "../hooks/context"
import { AuthForms } from "../components/ui/authForms"
import { Link, useNavigate } from "react-router"
import { loginService } from "../services/authService"
import {jwtDecode} from "jwt-decode"
import { AuthStructureLayout } from "../components/layout/AuthLayout.jsx"
import "../components/layout/authLayout.css"

export function LoginPage(){
    let navigate = useNavigate();
    const [credentials,setCredentials] = useState({
        email: "",
        password: ""
    });
    const [loading,setLoading] = useState(false);
    const [error,setError] = useState(null);
    const {user,setUser} = useUser();
    async function handleClick(){
        try{
            setLoading(true);
            setError(null);
            const email = credentials?.email.trim();
            const password = credentials?.password.trim(); 
            if(!email || !password){
                const error = new Error("Please fill all the necessary information.");
                error.code = "EMPTY_INFO";
                throw error;
            }
            const access_token = await loginService(credentials);
            const payload = jwtDecode(access_token);
            setUser({
              email:payload.user_information.username,
              id:payload.user_information.user_id,
              role:payload.user_information.role
            });
            setTimeout(()=>{
              navigate("/");
            },2000)
        }catch(e){
            setError({
                code: e?.code,
                message:e.message,
                variant:e?.category
            })
        }finally{
            setLoading(false);
        }
    }
    return (
           <>
            <AuthStructureLayout
              title= "Login Page"
              loading = {loading}
              error={error}
              success={user}  
              message={"Login successful!"}        
             >
                <AuthForms
                  func={handleClick}
                  credentials={credentials}
                  setCredentials={setCredentials}
                 />
              </AuthStructureLayout>
           <div className="support-links-box">
              <Link className="auth-support-link" to="/auth/requestreset" style={{textDecoration:"none"}}>Forgot password?</Link>
              <Link className="auth-support-link" to="/auth/register" style={{textDecoration:"none"}}>Don't have an account yet?</Link>
           </div>          
        </>
         
    )
}
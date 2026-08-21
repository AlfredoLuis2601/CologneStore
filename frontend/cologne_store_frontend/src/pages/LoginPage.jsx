import { useState } from "react"
import { useUser } from "../hooks/context"
import { AuthForms } from "../components/ui/authForms"
import { Link, useNavigate } from "react-router"
import { CircleCheck } from "lucide-react"
import { loginService } from "../services/authService"
import {jwtDecode} from "jwt-decode"
import ErrorUI from "../components/ui/errorState"

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
             <div className="auth-page-title-box">
               <h2 className="title">Login</h2>
             </div>
             <AuthForms func={handleClick} credentials={credentials} 
           setCredentials={setCredentials}
             />
           {user && (
            <div className="successfull-auth-box">
             <CircleCheck className="svg-check"/>
             <p className="successfull-auth-text">Login has been successfully done!</p>
            </div>
           )}
           {error && (
             <ErrorUI
               code={error.code}
               message={error.message}
               variant={error.variant}
               size="sm"
             />
           )}
           <div className="support-links-box">
              <Link className="auth-support-link" to="/auth/requestreset" style={{textDecoration:"none"}}>Forgot password?</Link>
              <Link className="auth-support-link" to="/auth/register" style={{textDecoration:"none"}}>Don't have an account yet?</Link>
           </div>          
        </>
         
    )
}
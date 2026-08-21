import { useEffect, useState } from "react";
import { AuthForms } from "../components/ui/authForms.jsx";
import { signUpService } from "../services/authService.js";
import { CircleCheck } from "lucide-react";
import { useVerifyMail } from "../hooks/context.jsx";
import { useNavigate } from "react-router";
import ErrorUI from "../components/ui/errorState.jsx";
export function SignUpPage(){
    const {isVerified} = useVerifyMail();
    const [credentials,setCredentials] = useState({
        email:"",
        password:""
    });
    let navigate = useNavigate();
    const [error,setError] = useState(null);
    const [loading,setLoading] = useState(false);
    const [created,setCreated] = useState(null);
    async function signUpHandler(){
        try{
            setLoading(true);
            const email = credentials.email?.trim();
            const password = credentials.password?.trim();
            if(!email || !password) {
                const error = new Error("Please fill all the necessary information.");
                error.code = "EMPTY_INFO";
                throw error;
            }
            await signUpService(credentials);
            setCreated(true);
        }catch(e){
           setError({
            code:e?.code,
            message:e.message,
            variant:e?.category
            })
           
        }finally{
            setLoading(false);
        }
    }
    if(isVerified){
        setTimeout(()=>{
           navigate("/auth")
        },2000)
    }
    return (
         <>
         {isVerified? (
           <div className="succesfull-verify">
              <CircleCheck className="svg-check-lg"/>
              <p className="sucessfull-auth-text-lg">
                Account has been succesfully verified!
              </p>
           </div>
        )
         :
         (<>
           <div className="auth-page-title-box">
            <h2>Sign Up</h2>
           </div>
           <AuthForms func={signUpHandler}
            credentials={credentials}
            setCredentials={setCredentials}
            />
         </>)
         }
         {created && (
            <div className="successfull-auth-box">
             <CircleCheck className="svg-check-sm"/>
             <p className="successfull-auth-text-sm">Account has been successfully created!</p>
            </div>
         )}
         {error && (
             <ErrorUI
               code={error.code}
               message={error.message}
               variant={error?.variant}
               size="sm"
             />
           )}
       </>
    )
}
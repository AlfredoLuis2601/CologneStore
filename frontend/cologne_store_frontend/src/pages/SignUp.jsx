import { useEffect, useState } from "react";
import { AuthForms } from "../components/ui/authForms.jsx";
import { signUpService } from "../services/authService.js";
import { CircleCheck } from "lucide-react";
import { useNavigate } from "react-router";
import { useVerifyMail } from "../hooks/context.jsx";
import { AuthStructureLayout } from "../components/layout/AuthLayout.jsx";
export function SignUpPage(){
    const [credentials,setCredentials] = useState({
        email:"",
        password:""
    });
    let navigate = useNavigate();
    const [error,setError] = useState(null);
    const [loading,setLoading] = useState(false);
    const [created,setCreated] = useState(null);
    const {isVerified,setIsVerified} = useVerifyMail();
    
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
            const newUser = await signUpService(credentials);
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
    useEffect(()=>{
     let timerId = null;
     const handleStorage = (event) =>{
        if(event.key == "verified" && event.newValue == "true"){
          localStorage.removeItem("verified");
          setIsVerified(true);
          timerId = setTimeout(()=>{
            navigate("/auth",{replace:true});
          },2500)
        }
     }
     window.addEventListener("storage",handleStorage);
     return () => {window.removeEventListener("storage",handleStorage);
       if(timerId){
      clearTimeout(timerId);
       }
    }
    },[navigate])
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
            <AuthStructureLayout
                title= "Sign Up"
                loading = {loading}
                error={error}
                success={created} 
                message="Account has been successfully created!"         
             >
              <AuthForms func={signUpHandler}
                credentials={credentials}
                setCredentials={setCredentials}
              />
            </AuthStructureLayout>
  
         </>)
       }
       </>
    )
}
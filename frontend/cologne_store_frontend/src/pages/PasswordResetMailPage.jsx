import {CircleCheck } from "lucide-react";
import { AuthMailForms } from "../components/ui/authForms.jsx"
import ErrorUI from "../components/ui/errorState.jsx";
import { LoadState } from "../components/ui/loadingState.jsx";
import { passwordResetMail } from "../services/authService.js";
import { useReset } from "../hooks/context.jsx";
import { AuthStructureLayout } from "../components/layout/AuthLayout.jsx";
import { useEffect,useState } from "react";
import { useNavigate } from "react-router";

// Alterar logica do handleSubmit 
export function RequestPasswordResetPage(){
    let navigate = useNavigate();
    const [email, setEmail] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const {reset,setReset} = useReset();

    async function handleClick(){

      try{
        setSuccess(false);
        setLoading(true);
        setError(null);
        const response = await passwordResetMail(email);
        console.log(response);
        setSuccess(true);
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

    useEffect(()=>{
      let timerId = null;
      const handleStorage = (event) =>{
        if(event.key == "reset" && event.newValue == "true"){
          localStorage.removeItem("reset");
          setReset(true);
          timerId = setTimeout(()=>{
            navigate("/auth",{replace:true})
          },2500)
        }
      }
      window.addEventListener("storage",handleStorage);
      return () => {
        window.removeEventListener("storage",handleStorage);
        if(timerId){
          clearTimeout(timerId);
        }
      }
    },[navigate])

    return(
        <>
        {reset? (
          <div className="succesfull-verify">
              <CircleCheck className="svg-check-lg"/>
              <p className="sucessfull-auth-text-lg">
                Redirecting to login page...
              </p>
           </div>
        ):(
          <AuthStructureLayout
            loading={loading}
            error={error}
            success={success}
            message="Email sent successfully!"
            title="Request Password Reset"
          >
           <AuthMailForms
              handleClick={handleClick}
              email={email}
              setEmail={setEmail}
           />
          </AuthStructureLayout>
        )
      } 
        </>
    )
}
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useVerifyMail } from "../hooks/context.jsx";
import { CircleCheck } from "lucide-react";
import { verifyMailService } from "../services/authService.js";
import ErrorUI from "../components/ui/errorState.jsx"
import { LoadState } from "../components/ui/loadingState.jsx";
export function VerifyMailPage(){
    const params = useParams();
    const key = params.key;
    const {isVerified,setIsVerified} = useVerifyMail(); 
    const [error,setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [resendSuccess,setRecendSuccess] = useState(false);
    //Add handleClick logic 
    useEffect(()=>{
     async function handleVerify(){
       try{
         setLoading(true);
         setError(null);
         const response = await verifyMailService(key);
         console.log(response);
         setIsVerified(true);
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
     handleVerify();
    },[])
    if(loading) return(
      <>
        <LoadState 
          message={"Loading..."}
          size={"lg"}
        />
     </>
    )
    return(
        <div className="verify-mail-box">
        {isVerified && (
            <div className="successfull-auth-box-lg">
            <CircleCheck className="svg-check-lg"/>
            <p className="succesfull-auth-text-lg">Account has 
            been succesfully verified
            </p>
            <p className="sucessfull-auth-text-lg">You can close this page now and go to Sign up page again.</p>
            </div>
        )}
        {error && (
            <>
            <ErrorUI
               code={error.code}
               message={error.message}
               variant={error.variant}
               size="lg"
             />
            </>
        )}
        {error?.code === "EMAIL_TOKEN_EXPIRED" && (
            <>
            <button className="resend-mail-button"></button>
            </>
        )}
        </div>
    )
}
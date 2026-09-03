import { useState } from "react";
import { useReset } from "../hooks/context";
import { useNavigate, useParams} from "react-router";
import { AuthPasswordForms } from "../components/ui/authForms";
import { LoadState } from "../components/ui/loadingState";
import ErrorUI from "../components/ui/errorState";
import { CircleCheck } from "lucide-react";
import { AuthStructureLayout } from "../components/layout/AuthLayout";
import { passwordResetService } from "../services/authService";


export function PasswordReset(){
    const params = useParams();
    const key = params.key;
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const {reset, setReset} = useReset();
    const [payload, setPayload] = useState({
        new_password: "",
        confirm_new_password: ""
    })
    async function handleClick(){
      setLoading(true);
      setError(null);
      try{
        const password = payload?.new_password.trim();
        const confirm_password = payload?.confirm_new_password.trim();
        if(!password || !confirm_password){
          const error = new Error("Please fill all the necessary information.");
          error.code = "EMPTY_INFO";
          throw error;
        }
        const response = await passwordResetService(payload, key);
        localStorage.setItem("reset","true");
        setReset(true);
        console.log(response);
      }catch(e){
        setError(
          {code: e?.code,
          message:e.message,
          variant:e?.category}
        );
      }
    }
    return(
        <>
          <AuthStructureLayout
            title= "Password Reset"
            loading = {loading}
            error={error}
            success={reset}   
            message="Password has been reset, you can close this page now"       
          >
            <AuthPasswordForms
              handleClick={handleClick}
              payload={payload}
              setPayload={setPayload}
            />
          </AuthStructureLayout>
        </>
    )
}
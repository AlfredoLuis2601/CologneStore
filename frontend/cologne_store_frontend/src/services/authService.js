import api from "./api.js"
import { errorHandler } from "../utils/apiErrorHandling.js"

export async function getNewAccessToken(refresh_token){
    try{   
      const token = await api.post("/users/refresh_token", refresh_token);
      localStorage.setItem("access_token", token)
      return token;
    }catch(e){
        errorHandler(e);
    }
}

export async function loginService(payload){
   try{
     const tokenPayload = await api.post("/users/signIn",
        {
         email:payload.email,
         hash_password:payload.password
        }
     )
     localStorage.setItem("access_token",tokenPayload.access_token);
     localStorage.setItem("refresh_token",tokenPayload.refresh_token);
     return tokenPayload.access_token;
   }catch(e){
     errorHandler(e);
   }
}

export async function signUpService(payload){

   try{
     const response = await api.post("/users/sign_up",{
        email:payload.email,
        hash_password:payload.password
     })
     return response;
   }catch(e){
     errorHandler(e);
   }
}

export async function verifyMailService(key){
    try{
      const response = await api.post(`/users/validate_account/${key}`);
      return response;
    }catch(e){
      errorHandler(e);
    }
}

export async function resendMailService(key){
  try{
    const response = await api.post("users/resend_mail",{
      key: key
    })
    return response;
  }catch(e){
    errorHandler(e);
  }
}
export async function logoutService(){
    
}

export async function passwordResetMail(email){
    try{
      const response = await api.post("users/password_reset",{
        email: email
      })
      return response;
    }catch(e){
      errorHandler(e);
    }
}

export async function passwordResetService(payload,key){
  try{
    const response = await api.post(`users/password_reset/${key}`,payload);
    return response;
  }catch(e){
    errorHandler(e);
  }
}
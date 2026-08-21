import api from "./api.js"
import { errorHandler } from "../utils/apiErrorHandling.js"

export async function getNewAccessToken(){
    try{
      const token = await api.post("/users/refresh_token");
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
   //Pagina do signUp depois de voce verificar o email, navigate 
   // para login
   try{
     const response = await api.post("/users/sign_up",{
        email:payload.email,
        hash_password:payload.password
     })
     console.log(response);
   }catch(e){
     errorHandler(e);
   }
}

export function verifyMailService(){
    
}

export async function logoutService(){
    
}
import axios from "axios"
import { getNewAccessToken } from "./authService.js"
//Começando a entender axios (conexão API com meu site)

const api = axios.create({
    baseURL:import.meta.env.VITE_BASE_URL,
    headers:{"X-Custom-Header":"foobar"},
    timeout:60000
});

export default api;


//Começar a criar os interceptors para authentication

api.interceptors.request.use((config)=>{
  console.log(config);
  const token = localStorage.getItem("access_token");
  if(token){
    config.headers.set("Authorization",`Bearer ${token}`);
  }
  return config;
},(error)=>{
   return Promise.reject(error);
});

api.interceptors.response.use(
    (response)=>{
    return response.data;
},
 async (error)=>{
  const originalRequest = error.config;
  if(error.response.data?.detail==="RefreshTokenToAccess" && !originalRequest._retry){
     originalRequest._retry = true;
  
  try{
    const token = await getNewAccessToken();
    originalRequest.headers.set("Authorization",`Bearer ${token}`);
    return api(originalRequest);
  }catch(InvalidToken){
     //Redirecionar para a janela de login e limpar token invalido 
     localStorage.clear();
     window.location.replace("/login");
     return Promise.reject(InvalidToken); //Interrompe o programa original para realocar para login
  }
}
  return Promise.reject(error); //Lança erro qualquer para minha service
 }
);
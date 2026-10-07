import axios from "axios"
import { getNewAccessToken } from "./authService.js"
//Começando a entender axios (conexão API com meu site)

const api = axios.create({
    baseURL:import.meta.env.VITE_BASE_URL,
    headers:{"X-Custom-Header":"foobar"},
    timeout:60000
});

export default api;



api.interceptors.request.use((config)=>{
  const token = localStorage.getItem("access_token");
  if (config.url.includes("/sales/order")) {
    console.log("Token recuperado do localStorage:", token);
    console.log("Authorization header:", config.headers.Authorization);
    debugger; 
  }
  if(token && token!= "undefined" && token!="null"){
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
},(error)=>{
   return Promise.reject(error);
});

api.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        // Se der 401, vamos apenas rejeitar o erro SEM apagar o localStorage por enquanto
        // para sabermos exatamente quem está gerando a falha.
        return Promise.reject(error);
    }
);
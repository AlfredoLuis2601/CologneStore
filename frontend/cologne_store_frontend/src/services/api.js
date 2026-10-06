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
  if (originalRequest.url.includes("/refresh_token")) { 
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token")
            delete api.defaults.headers.common["Authorization"];
            window.location.replace("/auth");
            return Promise.reject(error);
        }
  if(error.response?.status === 401 && !originalRequest._retry){
     originalRequest._retry = true;
  
  try{
    const token = await getNewAccessToken();
    originalRequest.headers.set("Authorization",`Bearer ${token}`);
    return api(originalRequest);
  }catch(InvalidToken){
     localStorage.removeItem("access_token");
     localStorage.removeItem("refresh_token");
      delete api.defaults.headers.common["Authorization"]
     window.location.replace("/auth");
     return Promise.reject(InvalidToken); 
  }
}
  return Promise.reject(error); 
 }
);
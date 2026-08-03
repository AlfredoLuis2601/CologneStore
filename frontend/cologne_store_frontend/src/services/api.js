import axios from "axios"
import { errorHandler } from "../utils/apiErrorHandling"
//Começando a entender axios (conexão API com meu site)

const api = axios.create({
    baseURL:import.meta.env.VITE_BASE_URL,
    headers:{"X-Custom-Header":"foobar"},
    timeout:10000
});

async function getColognes() {
    try{
      const response = await api.get("/products");
      return response;
    }catch(e){
      errorHandler(e);
    }
}


import { errorHandler } from "../utils/apiErrorHandling"
import api from "./api.js"

async function getColognes() {
    try{
      const response = await api.get("/products");
      return response?.data;
    }catch(e){
      errorHandler(e);
    }
}
export default getColognes;

export async function getCologneByName(name){
   try{
    const response = await api.get(`/${name}`);
    console.log("Request sent.");
    return response?.data;
   }catch(e){
    errorHandler(e);
   }
}
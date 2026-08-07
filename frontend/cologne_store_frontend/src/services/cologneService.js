import { errorHandler } from "../utils/apiErrorHandling"
import api from "./api.js"

async function getColognes() {
    try{
      const response = await api.get("/products");
      console.log(response.data)
      return response?.data;
    }catch(e){
      errorHandler(e);
    }
}
export default getColognes
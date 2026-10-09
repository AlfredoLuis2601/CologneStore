import { errorHandler } from "../utils/apiErrorHandling"
import api from "./api.js"

async function getColognes() {
    try{
      const response = await api.get("/products");
      return response;
    }catch(e){
      errorHandler(e);
    }
}
export default getColognes;

export async function getCologneByName(name){
   try{
    const response = await api.get(`/name/${name}`);
    return response;
   }catch(e){
    errorHandler(e);
   }
}

export async function getCologneById(id){
   try{
     const response = await api.get(`/${id}`);
     return response;
   }catch(e){
    errorHandler(e);
   }
}

export async function createOrder(saleData) {
  try{
  const response = await api.post("/sales/order",saleData);
  return response;
  }catch(e){
    errorHandler(e);
  }
}

export async function getOrders(){

  try{
    const response = await api.get("/sales/order");
    return response
  }catch(e){
    errorHandler(e);
  }
}
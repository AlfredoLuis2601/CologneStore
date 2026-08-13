import { useEffect, useState } from "react"

export function useService(serviceFn,params=null,dataType){
  const [error,setError] = useState(null);
  const [loading,setLoading] = useState(false);
  const [data,setData] = useState(dataType);

  useEffect(()=>{
    async function loadData(){
        try{
         setLoading(true);
         const data = params!==null? await serviceFn(params): await serviceFn();
         const isEmptyArray = Array.isArray(responseData) && responseData.length === 0;
        if (!responseData || isEmptyArray) {
          const error = new Error("Inventory is empty.");
          error.code = "EMPTY_INVENTORY";
          error.category = "NOT_FOUND";
          throw error;
        }
          console.log("Response has been succesfully returned!");
          setData(data);
        }catch(error){
            setError({
            code:error?.code,
            message:error.message,
            variant:error?.category
          })
        }finally{
            setLoading(false);
        }
    }   
    loadData();
  },[])
  return {data,loading,error};
}
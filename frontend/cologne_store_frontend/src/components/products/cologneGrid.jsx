import CologneCard from "./cologneCard.jsx"
import getColognes from "../../services/cologneService.js"
import { useEffect, useState } from "react"
import ErrorUI from "../ui/errorState.jsx"
import SkeletonCard from "../ui/loadingState.jsx"
export default function CologneGrid(){
   const [colognes,setColognes] = useState([]); // Começando em branco
   const [loading,setLoading] = useState(null);
   const [error,setError] = useState(null);
   
   useEffect(()=>{
     async function loadData(){
        try{
          setLoading(true)
          const colognes = await getColognes();
          if(colognes.length===0){
            const error = new Error("Inventory is empty.");
            error.code = "EMPTY_INVENTORY";
            error.variant = "NOT_FOUND";
            throw error;
          }
          console.log("Response has been succesfully returned!")
          setColognes(colognes);
        }catch(error){
          setError({
            code:error?.code,
            message:error.message,
            variant:error?.category
          })
        }finally{
         setLoading(null);
        }
     }
    loadData();
   },[])
   if(error) return(<ErrorUI code={error.code} message={error.message} variant={error.variant}/>)
   if(loading) return(<SkeletonCard/>) //Loading Skeleton
   return(
    <ul className="cologne-grid">
      {colognes.map(cologne=>{
        return(<CologneCard cologne={cologne} key={cologne.uid}/>)
      })}
    </ul>
   )
}

import { useEffect, useState } from "react";
import { useParams } from "react-router"
import { CologneDetails } from "../components/products/cologneDetails.jsx";
import {CartSection } from "../components/ui/addToCart.jsx";
import { getCologneById, getCologneByName } from "../services/cologneService.js";
import { LoadState } from "../components/ui/loadingState.jsx";
import { Header } from "../components/layout/Header.jsx";
import { useNavigate } from "react-router";

export function CologneDetailsPage(){
    
    const params = useParams();
    const id = params.uid
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [cologne, setCologne] = useState(null);
    const [cologneSearch,setCologneSearch] = useState('');
    localStorage.removeItem("cart");
    let navigate = useNavigate();
    
   async function onSearch(term){
      setCologneSearch(term);
        try{
          const cologneData = await getCologneByName(term);
          navigate(`/colognedetails/${cologneData.uid}`)
        }catch(error){
            setError({
            code:error?.code,
            message:error.message,
            variant:error?.category
            })
   }
  }
    useEffect(()=>{
        console.log(id);
        const loadData = async () =>{
          try{
            setLoading(true);
            setError(null);
            const data = await getCologneById(id);
            setCologne(data);
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
    },[id])
    if(loading) return <LoadState size={"lg"} message={"loading"}/>
    return(
        <>
          <Header onSearch={onSearch}/>
          {cologne && (
            <CologneDetails cologne={cologne}>
               <CartSection 
               cologne={cologne}
               />
            </CologneDetails>
          )}
        </>
    )
}
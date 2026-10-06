import { useEffect, useState } from "react";
import { useParams } from "react-router"
import { CologneDetails } from "../components/products/cologneDetails.jsx";
import {CartSection } from "../components/ui/addToCart.jsx";
import { getCologneById} from "../services/cologneService.js";
import { LoadState } from "../components/ui/loadingState.jsx";
import { Header } from "../components/layout/Header.jsx";
import { useCologneSearch } from "../hooks/useCologneSearch.jsx";

export function CologneDetailsPage(){
    
    const params = useParams();
    const id = params.uid
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [cologne, setCologne] = useState(null);
    const {searchError} = useCologneSearch();

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

    if(loading) return <LoadState size={"lg"} message={"Loading..."}/>
    if(error) return <ErrorUI 
              code={error.code} 
              message={error.message} 
              variant={error.variant}
              size="lg"
            />

    return(
        <>
          <Header/>
          {cologne && (
            <CologneDetails cologne={cologne}>
               <CartSection 
               cologne={cologne}
               />
            </CologneDetails>
          )}
          {searchError && (
            <ErrorUI 
              code={searchError.code} 
              message={searchError.message} 
              variant={searchError.variant}
              size="sm"
            />
          )}
        </>
    )
}
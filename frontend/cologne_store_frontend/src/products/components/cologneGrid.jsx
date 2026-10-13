import CologneCard from "./cologneCard.jsx"
import getColognes from "../cologneService.js"
import ErrorUI from "../../shared/components/errorState.jsx"
import "../style/cologneCard.css"
import { useService } from "../../shared/hooks/useFetch.jsx"
import { LoadState } from "../../shared/components/loadingState.jsx"

export default function CologneGrid(){
   const {data:colognes,loading,error} = useService(getColognes,null,[])
   if(loading) return <LoadState message={"Loading..."} size={"lg"}/>
   if(error) return <ErrorUI code={error.code} message={error.message} variant={error.variant} size="lg"/>
   return(
    <ul className="cologne-grid">
      {colognes.map(cologne=>{
        return(<CologneCard cologne={cologne} key={cologne.uid}/>)
      })}
    </ul>
   )
}

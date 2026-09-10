import CologneCard from "./cologneCard.jsx"
import getColognes from "../../services/cologneService.js"
import ErrorUI from "../ui/errorState.jsx"
import "./cologneCard.css"
import { useService } from "../../hooks/useFetch.jsx"
import { LoadState } from "../ui/loadingState.jsx"
export default function CologneGrid(){
   const {data:colognes,loading,error} = useService(getColognes,null,[])
   if(loading) return <LoadState message={"loading"} size={"lg"}/>
   if(error) return <ErrorUI code={error.code} message={error.message} variant={error.variant} size="lg"/>
   return(
    <ul className="cologne-grid">
      {colognes.map(cologne=>{
        return(<CologneCard cologne={cologne} key={cologne.uid}/>)
      })}
    </ul>
   )
}

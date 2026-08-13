import CologneCard from "./cologneCard.jsx"
import getColognes from "../../services/cologneService.js"
import {useEffect, useState } from "react"
import ErrorUI from "../ui/errorState.jsx"
import "./cologneGrid.css"
import "./cologneCard.css"
import { useService } from "../../hooks/useFetch.jsx"
import SkeletonCard from "../ui/loadingState.jsx"
export default function CologneGrid(){
   const {data:colognes,loading,error} = useService(getColognes,null,[])
   if(loading) return <SkeletonCard/>
   else if(error) return <ErrorUI code={error.code} message={error.message} variant={error.variant}/>
   return(
    <ul className="cologne-grid">
      {colognes.map(cologne=>{
        return(<CologneCard cologne={cologne} key={cologne.uid}/>)
      })}
    </ul>
   )
}

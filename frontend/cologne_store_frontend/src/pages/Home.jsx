import CologneGrid from "../components/products/cologneGrid.jsx"
import "../components/layout/Home.css"
import { getCologneByName } from "../services/cologneService.js"
import { useEffect, useState } from "react"
import { Header } from "../components/layout/Header.jsx"
import SkeletonCard from "../components/ui/loadingState.jsx"
import { useNavigate } from "react-router"
import ErrorUI from "../components/ui/errorState.jsx"
export default function Home(){
    const [loading,setLoading] = useState(false);
    const [error,setError] = useState(null);
    const [cologne,setCologne] = useState('');
    let navigate = useNavigate()
   async function onSearch(term){
      setCologne(term);
      console.log(term);
        try{
          setLoading(true);
          const cologne = await getCologneByName(term);
          console.log("You clicked the button!");
          navigate(`/colognedetails/${cologne.uid}`)
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
    return (
       <main className="home-container">
          <Header 
            onSearch={onSearch}
          />
          <section className = "home-box">
            {error && 
           (<ErrorUI 
              code={error.code} 
              message={error.message} 
              variant={error.variant}
            />
          )}
          <CologneGrid/>
        </section>
    </main>
 )
}
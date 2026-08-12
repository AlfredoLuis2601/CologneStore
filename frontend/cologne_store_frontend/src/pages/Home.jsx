import CologneGrid from "../components/products/cologneGrid.jsx"
import "../components/layout/Home.css"
import { getCologneByName } from "../services/cologneService.js"
import cologneImg from "../assets/home/cologne-logo.webp"
import { useEffect, useState } from "react"
import { Header } from "../components/layout/Header.jsx"
import SkeletonCard from "../components/ui/loadingState.jsx"
import { useNavigate } from "react-router"

export default function Home(){
    const [loading,setLoading] = useState(false);
    const [error,setError] = useState(null);
    const [cologne,setCologne] = useState('');
    //Para amanha reparar a API mudar a logica da criacao do perfume para ser sempre
    //minusculo e no get sempre transformar o body em minusculo tb
    //Começar component do login e ajustar o CSS
   async function onSearch(term){
      let navigate = useNavigate()
      setCologne(term);
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
          <section div className = "home-box">
            {error && 
           (<ErrorUI 
              code={error.code} 
              message={error.message} 
              variant={error.variant}
            />
          )}
          {loading && <SkeletonCard/>}
        {!loading && !error &&(
            <CologneGrid 
         loading={loading}
         setLoading={setLoading}
         error={error}
         setError={setError}
         />
        )}
        </section>
    </main>
 )
}
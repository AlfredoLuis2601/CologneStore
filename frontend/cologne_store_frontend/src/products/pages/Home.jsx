import CologneGrid from "../components/cologneGrid.jsx"
import "../style/Home.css"
import { Header } from "../../shared/components/Header.jsx"
import ErrorUI from "../../shared/components/errorState.jsx"
import { useCologneSearch } from "../../shared/hooks/useCologneSearch.jsx"

export default function Home(){
    const {searchError} = useCologneSearch();
    return (
       <main className="home-container">
          <Header/>
          <section className = "home-box">
            {searchError && 
           (<ErrorUI 
              code={searchError.code} 
              message={searchError.message} 
              variant={searchError.variant}
              size="sm"
            />
          )}
          <CologneGrid/>
        </section>
    </main>
 )
}
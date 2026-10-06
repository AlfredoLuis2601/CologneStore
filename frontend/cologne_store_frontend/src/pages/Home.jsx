import CologneGrid from "../components/products/cologneGrid.jsx"
import "../components/layout/Home.css"
import { Header } from "../components/layout/Header.jsx"
import ErrorUI from "../components/ui/errorState.jsx"
import { useCologneSearch } from "../hooks/useCologneSearch.jsx"

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
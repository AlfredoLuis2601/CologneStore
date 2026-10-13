import { HomeTitle } from "./Title.jsx"
import { SearchBar } from "./Search.jsx"
import "../style/Header.css"
import { useCologneSearch } from "../hooks/useCologneSearch.jsx"
import { Login } from "../../auth/components/Login.jsx";

export function Header(){
    
    const { cologneSearch, setCologneSearch, handleSearch} = useCologneSearch();
    return(
     <div className="header-container">
      <HomeTitle/>
      <SearchBar 
        searchTerm={cologneSearch}
        setSearchTerm={setCologneSearch}
        onSearch={handleSearch}
     />
     <Login/>
    </div>
    )
}
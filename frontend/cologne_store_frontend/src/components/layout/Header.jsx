import { useState } from "react"
import { HomeTitle } from "./Title.jsx"
import { SearchBar } from "./Search.jsx"
import "./Header.css"
import { useCologneSearch } from "../../hooks/useCologneSearch.jsx"
import { Login } from "../ui/Login.jsx";

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
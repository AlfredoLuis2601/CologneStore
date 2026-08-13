import { useState } from "react"
import { HomeTitle } from "./Title.jsx"
import { SearchBar } from "./Search.jsx"
import "./Header.css"
import { Login } from "../ui/Login.jsx";
export function Header({onSearch}){
    //Title(link para home), search bar e login 
    const [searchTerm,setSearchTerm] = useState('');
    return(
     <div className="header-container">
      <HomeTitle/>
      <SearchBar 
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        onSearch={onSearch}
     />
     <Login/>
    </div>
    )
}
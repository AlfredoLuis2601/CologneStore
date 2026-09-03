import { Search } from "lucide-react"
import { getCologneByName } from "../../services/cologneService.js"
export function SearchBar({searchTerm,setSearchTerm,onSearch}){
  function cologneOnChange(e){
     const name = e.target.value;
     const cleanName = name.trim();
     if (!cleanName) return;
     const urlSafeName = encodeURIComponent(cleanName);
     setSearchTerm(urlSafeName);
  }
  function handleDefault(e){
    e.preventDefault();
    onSearch(searchTerm);
  }

   return(
     <form className="search-box" onSubmit={handleDefault}>
       <input className="search-input"type="text" placeholder="Search:" value={searchTerm} onChange={cologneOnChange}/>
       <button className="search-button"type="submit"><Search/></button>
     </form>
   )
}
//Passar estado de loading e error para home (lifting up),
//tudo que é usado por varios components filhos deve ser feito isso
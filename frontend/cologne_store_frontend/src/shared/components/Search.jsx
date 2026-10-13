import { Search } from "lucide-react"

export function SearchBar({searchTerm,setSearchTerm,onSearch}){
  
  function handleDefault(e){
    e.preventDefault();
    const cleanName = searchTerm.trim();
    if(!cleanName) return ;
    const cleanNameUrl = encodeURIComponent(cleanName)
    onSearch(cleanNameUrl);
  }

   return(
     <form className="search-box" onSubmit={handleDefault}>
       <input className="search-input"type="text" placeholder="Search:" value={searchTerm} onChange={(e)=>setSearchTerm(e.target.value)}/>
       <button className="search-button"type="submit"><Search/></button>
     </form>
   )
}

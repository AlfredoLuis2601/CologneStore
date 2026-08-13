import priceCurrency from "../../utils/priceFormat.js"
import "./cologneCard.css"
import { Link } from "react-router"
function CologneCard({cologne}){
    //Add o component link para ir para a pagina /cologne:id/...id do perfume
   return(
    <Link to={`/colognedetails/${cologne.uid}`} style={{textDecoration:"none"}}>
    <li className="cologne-card"> 
    <article className ="cologne-box">
        <div className ="cologne-img-wrapper">
          <img className="cologne-img"src={cologne.image_url} alt={cologne.name}/>
        </div>
        <div className= "cologne-info">
         <div className="cologne-titles">
           <h2 className="cologne-name">{cologne.name}</h2>
           <p className="cologne-brand">{cologne.brand}</p>
         </div>
         <div className="sales-info">
           <p>{priceCurrency(cologne.price)}</p> 
         </div>
        </div>
    </article>
    </li>
    </Link>
   )
}

export default CologneCard 
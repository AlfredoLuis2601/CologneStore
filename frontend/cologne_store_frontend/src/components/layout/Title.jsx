import cologneImg from "../../assets/home/cologne-logo.webp"
import { Link } from "react-router"
import "./Header.css"
export function HomeTitle(){
    //Posteriormente envolver o container com o link para o home
    return(
        <Link to={"/"} style={{textDecoration:"none"}}>
        <div className = "title-container">
          <img className ="cologne-icon"src={cologneImg}></img>
          <h1 className="home-page-title">Cologne Store</h1>
        </div>
        </Link>
    )
}
import { Link } from "react-router"
import { CircleUser } from "lucide-react"
import "../layout/Login.css"
import { useUser } from "../../hooks/context.jsx"

export function Login(){
    const {user} = useUser();
    //Dependendo do valor de user o component login muda
    return(
        <>
        {!user && (
            <Link to={"/auth"} style={{textDecoration: "none", color: "white" }}>
        <div className="login-header-container">
          <CircleUser style={{color:"blue"}}/>
          <p className="login-header-text">Login</p>
        </div>
           </Link>      
        )}
        {user && (
            <img 
            src={`https://ui-avatars.com/api/?name=${user?.email}&background=random&color=fff`} 
            alt="Avatar do usuário" 
            className="user-avatar-image"
           />
        )}
        </>
    )
}


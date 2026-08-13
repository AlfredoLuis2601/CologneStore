import { Link } from "react-router"
import { CircleUser } from "lucide-react"
import "../layout/Login.css"

export function Login(){
    return(
        <Link>
        <div className="login-container">
          <CircleUser/>
          <p>Login</p>
        </div>
        </Link>
    )
}
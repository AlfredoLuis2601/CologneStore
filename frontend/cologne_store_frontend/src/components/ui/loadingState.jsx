import { LoaderCircle } from "lucide-react"
import "./loadState.css"
export function LoadState({message,size}){
  return (
    <div className = {`loading-box-${size}`}>
       <LoaderCircle/>
       <p className={`loading-message-${size}`}>{message}</p>
    </div>
  )
}

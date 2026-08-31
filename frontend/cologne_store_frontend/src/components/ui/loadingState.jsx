import { LoaderCircle } from "lucide-react"
import Skeleton from "react-loading-skeleton"

export function LoadState({message,size}){
  return (
    <div className = {`loading-box-${size}`}>
       <LoaderCircle/>
       <p className={`loading-message-${size}`}>{message}</p>
    </div>
  )
}

export default function SkeletonCard(){
  return(
      <li className="cologne-card"> 
      <article>
          <div className ="cologne-img-wrapper">
            <Skeleton/>
          </div>
          <div className= "cologne-info">
           <div className="cologne-titles">
             <Skeleton/>
             <Skeleton/>
           </div>
           <div className="sales-info">
             <Skeleton/>
           </div>
          </div>
      </article>
      </li>
     )
    }

function SkeletonGrid(){
    
}

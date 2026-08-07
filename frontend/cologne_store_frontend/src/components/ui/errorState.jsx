import {TriangleAlert,WifiOff,SearchX,ServerCrash, Icon} from "lucide-react"
function ErrorUI({code=null,message,variant="DEFAULT"}){
   const icons = {
     DEFAULT:TriangleAlert,
     NETWORK:WifiOff, //request (cors, sem internet)
     NOTFOUND:SearchX,
     SERVER_ERROR:ServerCrash 
   }
   const IconComponent = icons[variant];
   return (
    <div className="error-container">
      <IconComponent size={48} className="error-icon"/>
      <p>{code}</p>
      <p>{message}</p>
    </div>
   )
}
export default ErrorUI


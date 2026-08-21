import {TriangleAlert,Ban,WifiOff,SearchX,ServerCrash, Icon,ShieldAlert} from "lucide-react"
function ErrorUI({code=null,message,variant="DEFAULT",size="md"}){
   const icons = {
     DEFAULT:TriangleAlert,
     NETWORK:WifiOff, //request (cors, sem internet)
     NOT_FOUND:SearchX,
     SERVER_ERROR:ServerCrash,
     UNAUTHORIZED:ShieldAlert,
     FORBIDDEN:Ban
   }
   const IconComponent = icons[variant];
   return (
    <div className={`error-container-${size}`}>
      <IconComponent className={`error-icon-${size}`}/>
      <p className={`error-message-${size}`}>{message}</p>
    </div>
   )
}
export default ErrorUI


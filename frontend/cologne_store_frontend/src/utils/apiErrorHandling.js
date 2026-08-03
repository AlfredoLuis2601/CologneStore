import axios from "axios"

export function errorHandler(e){
   if(e.response){
      const status = e.response.status;
      const detail = e.response.data?.detail;
      switch(status){
        case 400:{
            if(detail.error_code === "DifferentPasswords"){
              const error = new Error(detail.error_message);
              error.code = "DIFFERENT_PASSWORDS";
              throw error;
            }else if(detail.error_code === "UserAlreadyVerified"){
              const error = new Error(detail.error_message);
              error.code = "USER_ALREADY_VERIFIED";
              throw error;
            }else{
              const error = new Error("Bad request to the server");
              error.code = "BAD_REQUEST";
              throw error;
            }
        }
        case 401:{
           if(detail.error_code === "InvalidToken"){
             const error = new Error("Login credentials expired.");
             error.code = "INVALID_TOKEN";
             throw error;
           }else if(detail.error_code === "RefreshTokenToAcess"){
             const error = new Error("Provide a new acess token.");
             error.code = "REFRESH_TOKEN_TO_ACESS";
             throw error;
           }else if(detail.error_code === "TokenAlreadyInBlackList"){
             const error = new Error(detail.error_message ||"Credentials in the black list.");
             error.code = "TOKEN_BLACK_LIST";
             throw error;
           }else if(detail.error_code === "RolePermission"){
            const error = new Error(detail.error_message);
            error.code = "ROLE_PERMISSION_UNAUTHORIZED"
            throw error;
           }else if(detail.error_code === "EmailNotVerified"){
             const error = new Error(detail.error_message);
             error.code = "EMAIL_NOT_VERIFIED"
             throw error;
           }else if(detail.error_code === "EmailTokenExpired"){
             const error = new Error(detail.error_message);
             error.code = "EMAIL_TOKEN_EXPIRED";
             throw error;
           }
           break;
        }
        case 403:{
            const error = new Error(detail.error_message);
            error.code = "USER_ALREADY_EXISTS";
            throw error;
        }
        case 404:{
           if(detail.error_code === "UserNotFound"){
             const error = new Error(detail.error_message);
             error.code = "USER_NOT_FOUND";
             throw error;
           }else if(detail.error_code === "CologneNotFound"){
            const error = new Error(detail.error_message);
            error.code = "COLOGNE_NOT_FOUND";
            throw error;
           }
            else if (detail.error_code === 'EmptyInventory') {
            const error = new Error(detail.error_message || 'Empty Inventory');
            error.code = 'EmptyInventory';
            throw error;
           }else if(detail.error_code === "DeleteCologne"){
            const error = new Error(detail.error_message);
            error.code = "DELETE_COLOGNE_NOT_FOUND";
            throw error;
           }
        }
        default:{
          throw new Error("Generic error.")
        }
      }
   }else if(e.code){ //They don't need specific treatment as the response ones so I didnt add error code to them
     const code = e.code;
     switch(code){
        case "ERR_NETWORK":{
           throw new Error("Connection with the server failed, check the backend connection.");
        }
        case "ECONNABORTED":{
           throw new Error("Request has been timed out.Try again.");
        }
     }
   }
}
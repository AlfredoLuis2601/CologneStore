import axios from "axios"

export function errorHandler(e){
   if(e.response){
      const status = e.response.status;
      const detail = e.response.data?.detail;
      switch(status){
        case 400:{
            if(detail.error_code === "DifferentPasswords"){
              const error = new Error(detail.error_message,{cause:e});
              error.code = "DIFFERENT_PASSWORDS";
              throw error;
            }else if(detail.error_code === "UserAlreadyVerified"){
              const error = new Error(detail.error_message,{cause:e});
              error.code = "USER_ALREADY_VERIFIED";
              throw error;
            }else{
              const error = new Error("Bad request to the server",{cause:e});
              error.code = "BAD_REQUEST";
              throw error;
            }
        }
        case 401:{
           if(detail.error_code === "InvalidToken"){
             const error = new Error("Login credentials expired.",{cause:e});
             error.code = "INVALID_TOKEN";
             error.category = "UNAUTHORIZED";
             throw error;
           }else if(detail.error_code === "RefreshTokenToAcess"){
             const error = new Error("Provide a new acess token.",{cause:e});
             error.code = "REFRESH_TOKEN_TO_ACESS";
             error.category = "UNAUTHORIZED";
             throw error;
           }else if(detail.error_code === "TokenAlreadyInBlackList"){
             const error = new Error(detail.error_message ||"Credentials in the black list.",{cause:e});
             error.code = "TOKEN_BLACK_LIST";
             error.category = "UNAUTHORIZED";
             throw error;
           }else if(detail.error_code === "RolePermission"){
            const error = new Error(detail.error_message,{cause:e});
            error.code = "ROLE_PERMISSION_UNAUTHORIZED";
            error.category = "UNAUTHORIZED";
            throw error;
           }else if(detail.error_code === "EmailNotVerified"){
             const error = new Error(detail.error_message,{cause:e});
             error.code = "EMAIL_NOT_VERIFIED";
             error.category = "UNAUTHORIZED";
             throw error;
           }else if(detail.error_code === "EmailTokenExpired"){
             const error = new Error(detail.error_message,{cause:e});
             error.code = "EMAIL_TOKEN_EXPIRED";
             error.category = "UNAUTHORIZED";
             throw error;
           }
           break;
        }
        case 403:{
            const error = new Error(detail.error_message,{cause:e});
            error.code = "USER_ALREADY_EXISTS";
            error.category = "FORBIDDEN";
            throw error;
        }
        case 404:{
           if(detail.error_code === "UserNotFound"){
             const error = new Error(detail.error_message,{cause:e});
             error.code = "USER_NOT_FOUND";
             error.category = "NOT_FOUND";
             throw error;
           }else if(detail.error_code === "CologneNotFound"){
            const error = new Error(detail.error_message,{cause:e});
            error.code = "COLOGNE_NOT_FOUND";
            error.category = "NOT_FOUND";
            throw error;
           }
            else if (detail.error_code === 'EmptyInventory') {
            const error = new Error(detail.error_message || 'Empty Inventory',{cause:e});
            error.code = 'EmptyInventory';
            error.category = "NOT_FOUND";
            throw error;
           }else if(detail.error_code === "DeleteCologne"){
            const error = new Error(detail.error_message,{cause:e});
            error.code = "DELETE_COLOGNE_NOT_FOUND";
            error.category = "NOT_FOUND";
            throw error;
           }
        }
        default:{
          throw e;
        }
      }
   }else if(e.code){ //They don't need specific treatment as the response ones so I didnt add error code to them
     const code = e.code;
     switch(code){
        case "ERR_NETWORK":{
           const error = new Error("Connection with the server failed, check the backend connection.",{cause:e});
           error.category = "NETWORK";
        }
        case "ECONNABORTED":{
           throw new Error("Request has been timed out.Try again.",{cause:e});
           error.category = "NETWORK";
        }
     }
   }
}
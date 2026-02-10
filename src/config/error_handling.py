#Create here classes for every error, and then make a function which will have as parameters 
#classes like this, for give a custom error handling for every problem in your application.
from typing import Any,Callable,List
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
class ErrorHandling(Exception):
    """
     Class designed to handle all the application errors.
    """
    
    pass

#Users error handling

class UserNotFound(ErrorHandling):
    """
    Error raised when the user was not found in the database.
    """
    pass

class UserAlreadyExist(ErrorHandling):
    """
    Error raised when the user information is already been used by other customer.
    """
    pass

class WrongPassword(ErrorHandling):
    """
    Error raised when the user account exists,but the password was wrong.
    """
    pass

#JWT and Security error handling:

class InvalidToken(ErrorHandling):
    """
    Error raised for invalid or expired tokens.
    """
    pass

class RefreshTokenToAccess(ErrorHandling):
    """
    Error raised when the client tries to access the server routes with a refresh token instead of a acces token.
    """
    pass

class TokenAlreadyInBlackList(ErrorHandling):
    """
    Error raised when the client tries to access the server routes after the logout is done.
    """
    pass

class GenerateRefresh(ErrorHandling):
    """
    Error raised when the refresh token expires.
    """
    pass

class RolePermission(ErrorHandling):
    """
    Error handler for insufficient role permision.
    """
    def __init__(self,required_role:List[str],user_role:str):
        self.required_role =required_role,
        self.user_role = user_role
    pass

#Cologne Errors:

class EmptyInventory(ErrorHandling):
    """
    Error for trying to get a cologne with an empty inventory.
    """
    pass

class CologneNotFound(ErrorHandling):
    """
    Cologne not found error.
    """
    pass

class DeleteCologne(ErrorHandling):
    """
    Cologne could not be deleted because it was not found.
    """
    pass
class EmailNotVerified(ErrorHandling):
    """Email has not been verified yet."""
    pass
class EmailTokenExpired(ErrorHandling):
    """Email token expired."""
class DifferentPassword(ErrorHandling):
    """The confirmed password was different than the previous one."""
def create_exception_handler(status_code:int,detail:Any)->Callable[[Request,Exception],JSONResponse]:
    #Request seria todo o request body retornado e a exception seria a minha custom exception lançada
    async def exception_handler(request:Request,exc:Exception)->JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content=detail
        )
    return exception_handler
    
def create_unauthorized_exception_handler(status_code:int,detail:dict)->Callable[[Request,RolePermission],JSONResponse]:
    async def unauthorized_exception_handler(request:Request,exc:RolePermission)->JSONResponse:
        exception_dict:dict = exc.__dict__
        return JSONResponse(
            status_code=status_code,
            content={
                "detail":detail,
                "path":request.url.path,
                "header":dict(request.headers),
                "client":request.client.host,
                "user_role":exception_dict.get("user_role"),
                "required_role":exception_dict.get("required_role")
            }
        ) 
    return unauthorized_exception_handler

def add_all_exceptions(my_app:FastAPI):
  my_app.add_exception_handler(UserNotFound,create_exception_handler(
    status_code=404,
    detail={
        "message":"User was not found,please provide a new user information.",
        "error_code":"UserNotFound"
    }
))
  my_app.add_exception_handler(UserAlreadyExist,create_exception_handler(
    status_code=403,
    detail={
        "error_message":"There is already a user with this account information.",
        "resolution":"Please provide new user information",
        "error_code":"UserAlreadyExists"
    }
))
  my_app.add_exception_handler(WrongPassword,create_exception_handler(
    status_code=422,
    detail={
        "error_message":"Wrong password.",
        "resolution":"Please provide another password.",
        "error_code":"WrongPassword"
    }
))
  my_app.add_exception_handler(CologneNotFound,create_exception_handler(
    status_code=404,
    detail={
        "error_message":"Cologne was not found in the inventory.",
        "resolution":"Please search again.",
        "error_code":"CologneNotFound"
    }
))
  my_app.add_exception_handler(EmptyInventory,create_exception_handler(
    status_code=404,
    detail={
        "error_message":"Cologne was not found because the inventory is empty",
        "resolution":"Restock",
        "error_code":"EmptyInventory"
    }
))
  my_app.add_exception_handler(DeleteCologne,create_exception_handler(
    status_code=404,
    detail={
        "error_message":"Cologne could not be deleted because it was not found.",
        "error_code":"DeleteCologne"
    }
))
  my_app.add_exception_handler(InvalidToken,create_exception_handler(
    status_code=401,
    detail={
        "error_message":"Expired or invalid token",
        "resolution":"User need to login again",
        "error_code":"InvalidToken"
    }
))
  my_app.add_exception_handler(RefreshTokenToAccess,create_exception_handler(
    status_code=401,
    detail={
        "error_message":"Refresh token to access the application routes.",
        "resolution":"Provide a new access token.",
        "error_code":"RefreshTokenToAccess"
    }
))
  my_app.add_exception_handler(TokenAlreadyInBlackList,create_exception_handler(
    status_code=401,
    detail={
        "error_message":"Revoked token to access the app routes.",
        "resolution":"User need to login again.",
        "error_code":"TokenAlreadyInBlackList"
    }
))
  my_app.add_exception_handler(GenerateRefresh,create_exception_handler(
    status_code=401,
    detail={
        "error_message":"Access token provided to the generate new_access_token route.",
        "resolution":"User need to login again.",
        "error_code":"GenerateRefresh"
    }
))
  my_app.add_exception_handler(RolePermission,create_unauthorized_exception_handler(
    status_code=401,
    detail={
        "error_message":"Unauthorized role for the route.",
        "error_code":"RolePermission"
    }
))
  my_app.add_exception_handler(EmailNotVerified,create_exception_handler(
      status_code=401,detail={
          "error_message":"Email has not been verified yet.",
          "solution":"Please go to email,check the email sent and verify your account.",
          "error_code":"EmailNotVerified"
      }
  ))
  my_app.add_exception_handler(EmailTokenExpired,create_exception_handler(
      status_code=401,detail={
          "error_message":"Email token expired.",
          "solution":"Please verify your email accessing the new email sent",
          "error_code":"EmailTokenExpired"
      }
  ))
  my_app.add_exception_handler(DifferentPassword,create_exception_handler(
      status_code=404,detail={
          "error_message":" User sent different passwords",
          "solution":"Type the password again.",
          "error_code":"DifferentPasswords"
      }
  ))
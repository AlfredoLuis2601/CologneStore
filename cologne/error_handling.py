#Create here classes for every error, and then make a function which will have as parameters 
#classes like this, for give a custom error handling for every problem in your application.
from typing import Any,Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse

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
    def __init__(self,role:str,user_info:dict):
        self.role = role,
        self.user_info = user_info
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
        required_role = exception_dict.get("role")
        return JSONResponse(
            status_code=status_code,
            content={
                "detail":detail,
                "path":request.url.path,
                "header":dict(request.headers),
                "client":request.client.host,
                "user_role":required_role,
                "required_role":"admin"
            }
        ) 
    return unauthorized_exception_handler
        
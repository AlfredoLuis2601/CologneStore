from fastapi import FastAPI
from cologne.routes import cologne_routes
from contextlib import asynccontextmanager
from cologne.database import start_db
from .user_routes import customer_routes
from cologne.error_handling import EmptyInventory,UserAlreadyExist,UserNotFound,TokenAlreadyInBlackList,InvalidToken,RefreshTokenToAccess,CologneNotFound,DeleteCologne,WrongPassword,RolePermission,GenerateRefresh,create_exception_handler,create_unauthorized_exception_handler
@asynccontextmanager
async def lifespan(app:FastAPI):
   print("Application has been initialized...")
   await start_db()
   yield
   print("Finishing application...")
api_version = "v1"
my_app = FastAPI(
    title="Cologne Store",
    description="Cologne Store REST API Simulation",
    lifespan=lifespan,
    version=api_version
)
my_app.include_router(cologne_routes,prefix=f"/api/{api_version}/cologne_store")
my_app.include_router(customer_routes,prefix=f"/api/{api_version}/cologne_store/users")

#Adding custom exception handler to the application 

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
#Include the routes and the endpoint prefix to the application.
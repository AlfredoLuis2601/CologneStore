from fastapi import FastAPI
from cologne.routes import cologne_routes
from contextlib import asynccontextmanager
from cologne.database import start_db
from .user_routes import customer_routes
from cologne.error_handling import add_all_exceptions
from cologne.middleware import adding_trusted_host_middleware,create_middleware,adding_CORS_middleware
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

add_all_exceptions(my_app)
adding_trusted_host_middleware(my_app)
create_middleware(my_app)
adding_CORS_middleware(my_app)
#Include the routes and the endpoint prefix to the application.

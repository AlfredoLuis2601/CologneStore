from fastapi import FastAPI
from cologne.routes import cologne_routes
from contextlib import asynccontextmanager
from cologne.database import start_db
from .user_routes import customer_routes
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

#Include the routes and the endpoint prefix to the application.
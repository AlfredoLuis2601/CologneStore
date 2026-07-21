from fastapi import FastAPI
from src.cologne.routes import cologne_router
from contextlib import asynccontextmanager
from src.config.database import start_db
from src.auth.routes import customer_routes
from src.sales.routes import sales_router
from src.config.error_handling import add_all_exceptions
from src.config.middleware import adding_trusted_host_middleware,create_middleware,adding_CORS_middleware
@asynccontextmanager
async def lifespan(app:FastAPI):
   print("Application has been initialized...")
   await start_db()
   yield
   print("Finishing application...")
api_version = "v1"
tags_metadata = [ {
        "name": "Colognes",
        "description": "Gerenciamento do catálogo de perfumes, controle de estoque e buscas.",
    },
    {
        "name": "Auth",
        "description": "Operações de autenticação, registro de clientes e gerenciamento de tokens.",
    },
    {
        "name": "Sales",
        "description": "Processamento de checkout, pedidos e histórico transacional.",
    }
]
my_app = FastAPI(
    title="Cologne Store",
    description="Cologne Store REST API",
    lifespan=lifespan,
    version=api_version,
    license_info={
        "name":"MIT",
        "url":"https://opensource.org/licenses/mit"
    },
    openapi_tags=tags_metadata,
    docs_url=f"/api/{api_version}/docs",
    contact={
        "email":"luisalfredoalvesdeandrade1010@gmail.com"
    }
)

my_app.include_router(cologne_router,prefix=f"/api/{api_version}/cologne_store",tags=["Colognes"])
my_app.include_router(customer_routes,prefix=f"/api/{api_version}/cologne_store/users",tags=["Auth"])
my_app.include_router(sales_router,prefix=f"/api/{api_version}/cologne_store/sales",tags=["Sales"])
#Adding custom exception handler to the application 

add_all_exceptions(my_app)
adding_trusted_host_middleware(my_app)
create_middleware(my_app)
adding_CORS_middleware(my_app)
#Include the routes and the endpoint prefix to the application.


from fastapi import FastAPI
from fastapi.requests import Request
import time 
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
def create_middleware(my_app:FastAPI):
 @my_app.middleware("http")
 async def register_middleware(request:Request,call_next): # request and the route(call_next)
    before = time.time()
    response = await call_next(request)
    after = time.time()
    print(f"{request.method} request to the {request.url.path} has been approved after {after-before} seconds.")
    
    return response
 return register_middleware
#ASGI custom middleware
def adding_trusted_host_middleware(app:FastAPI):
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=["*"])
    #allowing all hosts by now.
origins =     [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]
def adding_CORS_middleware(app:FastAPI):
    app.add_middleware(
        CORSMiddleware,allow_origins=origins,allow_headers=["*"],allow_methods=["*"]
    )
    

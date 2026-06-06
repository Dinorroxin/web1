"""
This is the starting point of the application, it creates an instance of FastAPI, includes the authentication routes defined in auth.py 
and defines a root route that returns some basic information about the API.
"""

from fastapi import FastAPI
from app.database import unique_email
from app.api.auth import router

app = FastAPI()

# Include_router is a FastAPI method that allows us to include the routes defined in the auth.py file, this way we can keep our code organized and modular
app.include_router(router)

# It will set the "main" route root to return a JSON with the title, description and version of the API
@app.get("/")
def read_root():
    return {
        "title": "API de Contabilidade",
        "description": "API para gerenciamento de clientes, fornecedores, contas a pagar e receber",
        "version": "1.0.0"
    }


# When starting the application, it will call the function unique_email to create the unique index on the email field of the users collection
@app.on_event("startup")
async def startup_event():
    await unique_email()
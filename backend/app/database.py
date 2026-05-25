import sys
import time
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# If doens't get the MONGO_URL it will print an error and exit
if not settings.MONGO_URL:
    print("ERRO CRÍTICO: A variável de ambiente MONGO_URL não está definida. Verifique o arquivo .env.")
    print("Verique se o arquivo .env ou config está puxando o .env corretamente antes de rodar a aplicação.")
    sys.exit(1)

# If gets the MONGO_URL from the .env file, it will create a MongoDB client
url = settings.MONGO_URL

client = AsyncIOMotorClient(url)
# The name of the database
db = client["dbContabilidade"]

def getdatabase():
    return db

async def unique_email():
    try:
        # Will create the collection users with the unique index email
        await db.users.create_index("email", unique=True)
    except Exception:
        pass
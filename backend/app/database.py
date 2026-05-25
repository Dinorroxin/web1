import sys
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# If doens't get the MONGO_URL it will print an error and exit
if not settings.MONGO_URL:
    print("ERRO CRÍTICO: A variável de ambiente MONGO_URL não está definida. Verifique o arquivo .env.")
    print("Verique se o arquivo .env ou config está puxando o .env corretamente antes de rodar a aplicação.")
    sys.exit(1)

# If gets the MONGO_URL from the .env file, it will create a MongoDB client
uri = settings.MONGO_URL

client = AsyncIOMotorClient(uri)
# The name of the database
db = client["dbContabilidade"]

def getdatabase():
    return db

async def unique_email():
    try:
        # If the email is already in use it wont allow to create a new user with the same email
        await db.users.create_index("email", unique=True)
    except Exception:
        pass
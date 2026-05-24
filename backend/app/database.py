import sys
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# If doens't get the MONGO_URL i will print an error and exit
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
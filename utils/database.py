from motor.motor_asyncio import AsyncIOMotorClient

async def get_db():
    uri = "mongodb://academia:academia@localhost:27017"
    client = AsyncIOMotorClient(uri)

    return client.academia
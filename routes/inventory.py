from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorDatabase

from fastapi import APIRouter, Depends

from models.inventory import CreateInventory, GetInventory
from utils.database import get_db
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId

router = APIRouter(
    prefix = "/inventory",
    tags=[
        "inventory"
    ],
)

@router.post("")
async def create_inventory(
    create_inventory: CreateInventory,
    database: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
):
    inserted_id = await database.inventory.insert_one(
        {
            "_id": str(ObjectId()),
            "name": create_inventory.name,
            "price": create_inventory.price,
            "category": create_inventory.category,
        }
    )
    return JSONResponse(
            content={"created_inventory": inserted_id.inserted_id},
            status_code=201
        )



@router.get("")
async def list_inventory(database: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
    inventory_list = [inventory async for inventory in database.inventory.find({})]

    return JSONResponse(
        content=jsonable_encoder(inventory_list),
        status_code=200
    )


@router.get("/{inventory_id}")
async def get_inventory(
    database : Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    inventory_id : str,
):
    inventory = await database.inventory.find_one(
        {
            "_id": inventory_id,
        }
    )

    if inventory:
        return JSONResponse(
            content=inventory,
            status_code=200
        )
    else:
        return JSONResponse(
            content={"message": "El producto no existe"},
            status_code=404
        )
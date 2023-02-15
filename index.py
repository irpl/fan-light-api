import os
from fastapi import FastAPI, Request
import motor.motor_asyncio
from bson import ObjectId
import pydantic

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.things

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

@app.get("/")
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.put("/api/toggle")
async def toggle(request: Request): 
  state = await request.json()

  lights_obj = await db["lights"].find_one({"thing":"lights"})
  if lights_obj:
    await db["lights"].update_one({"$set": state})
  else:
    await db["lights"].insert_one({**state, "thing": "lights"})
    new_ligts_obj = await db["lights"].find_one({"thing":"lights"}) 

  return new_ligts_obj
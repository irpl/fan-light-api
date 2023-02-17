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

  lights_obj = await db["hub"].find_one({"thing":"state"})
  if lights_obj:
    await db["hub"].update_one({"thing":"state"}, {"$set": state})

  else:
    await db["hub"].insert_one({**state, "thing": "state"})
  
  new_ligts_obj = await db["hub"].find_one({"thing":"state"}) 

  return new_ligts_obj

@app.put("/api/state")
async def get_state():
  state = await db["hub"].find_one({"thing": "state"})
  return state

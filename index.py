import os
from fastapi import FastAPI, Request
import motor.motor_asyncio
from bson import ObjectId
import pydantic

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://ecse-fan-light-client.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.things

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

@app.get("/")
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.put("/api/state")
async def toggle(request: Request): 
  state = await request.json()

  lights_obj = await db["hub"].find_one({"thing":"state"})
  if lights_obj:
    await db["hub"].update_one({"thing":"state"}, {"$set": state})

  else:
    await db["hub"].insert_one({**state, "thing": "state"})
  
  new_ligts_obj = await db["hub"].find_one({"thing":"state"}) 

  return new_ligts_obj

@app.get("/api/state")
async def get_state():
  state = await db["hub"].find_one({"thing": "state"})
  if state == None:
    return {"lights": False, "fan": False}
  return state

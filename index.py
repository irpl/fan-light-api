import os
from fastapi import FastAPI, Request
import motor.motor_asyncio
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated

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


class State(BaseModel):
  fan: bool
  lights: bool
        
state: State = {}

@app.get("/")
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.put("/api/state")
async def toggle(state_request: State): 
  global state

  state = state_request

  return state

@app.get("/api/state")
async def get_state():
  return state

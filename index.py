from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.put("/api")
async def toggle(request: Request): 
  return await request.json()
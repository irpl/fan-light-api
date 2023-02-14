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

if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000)
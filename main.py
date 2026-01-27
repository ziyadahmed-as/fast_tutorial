import fastapi
import fastapi.params
from typing import Optional


api = fastapi.FastAPI()

@api.get("/")
async def root():
    return {"message": "Hello World"}
@api.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
@api.post("/items/")
async def create_item(name: str = fastapi.Form(...), description: Optional[str] = None):
    return {"name": name, "description": description}
 
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000) 
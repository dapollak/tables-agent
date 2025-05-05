from fastapi import FastAPI
import uvicorn

from api.agent import get_number
from api.schemas import Tables
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get-table-number/{name}", response_model=Tables)
async def get_table_number(name: str) -> Tables:
    return await get_number(name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

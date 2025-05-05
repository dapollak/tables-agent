from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from agent import get_number
from schemas import Tables
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/api/get-table-number/{name}", response_model=Tables)
async def get_table_number(name: str) -> Tables:
    return await get_number(name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

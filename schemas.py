from pydantic import BaseModel

class Table(BaseModel):
    name: str
    hebrew_name: str
    table_number: int

class Tables(BaseModel):
    tables: list[Table]
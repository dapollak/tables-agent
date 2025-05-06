from pydantic import BaseModel

class Person(BaseModel):
    name: str
    hebrew_name: str
    table_number: int
    coming: bool

class People(BaseModel):
    people: list[Person]

class SimilarNames(BaseModel):
    similar_names: list[str]
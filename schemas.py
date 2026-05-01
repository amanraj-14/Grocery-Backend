from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: int
    category: str
    image: str

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True
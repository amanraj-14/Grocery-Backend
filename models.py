from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    category = Column(String)
    image = Column(String)


class CartItem(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)


# ✅ THIS MUST BE PRESENT
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
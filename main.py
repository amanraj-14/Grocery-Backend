from fastapi import FastAPI, Depends, Request, Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Product, CartItem, User
from schemas import ProductCreate, ProductResponse
from seed import seed_products
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import razorpay
import smtplib
from email.mime.text import MIMEText
import os

from auth import hash_password, verify_password, create_token


# ---------------- DB INIT ----------------
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB SESSION ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "Grocery API running 🚀"}

# ---------------- PRODUCTS ----------------
@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.post("/add-product", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    seed_products(db)
    return {"message": "30 products added successfully"}

# ---------------- CART ----------------
class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    name: str
    price: int
    quantity: int


@app.post("/cart")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):

    existing_item = db.query(CartItem).filter(
        CartItem.product_id == item.product_id,
        CartItem.user_id == item.user_id
    ).first()

    if existing_item:
        existing_item.quantity += item.quantity
    else:
        db.add(CartItem(**item.dict()))

    db.commit()
    return {"message": "Cart updated successfully"}


@app.get("/cart/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


@app.delete("/cart/{user_id}")
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": "Cart cleared"}

# ---------------- AUTH ----------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class LoginData(BaseModel):
    email: str
    password: str


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        return {"error": "Email already exists"}

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful",
        "user_id": new_user.id
    }


@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": user.id})

    return {
        "message": "Login successful",
        "user_id": user.id,
        "token": token
    }

# ---------------- CONTACT EMAIL ----------------
class Contact(BaseModel):
    name: str
    email: str
    message: str


# 👇 DIRECT EMAIL CONFIG (NO .env)
EMAIL_USER = "amanr835222@gmail.com"
EMAIL_PASS = "yxruhdchrosrkzbc"


@app.post("/contact")
async def send_contact(data: Contact):

    try:
        msg = MIMEText(f"""
New Contact Message

Name: {data.name}
Email: {data.email}
Message: {data.message}
""")

        msg["Subject"] = "New Contact Form Message"
        msg["From"] = EMAIL_USER
        msg["To"] = "amanr835222@gmail.com"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("amanr835222@gmail.com", "yxruhdchrosrkzbc")

        server.send_message(msg)
        server.quit()

        return {"message": "Email sent successfully ✅"}

    except Exception as e:
        return {"error": str(e)}

# ---------------- RAZORPAY ----------------

client = razorpay.Client(auth=(
    "rzp_test_SVoZ2GmFSGHSS5",   # test key_id
    "1nkIsTQ6RDXjkYt1glr6fzjK"     # test key_secret
))


@app.post("/create-order")
def create_order(data: dict = Body(...)):
    amount = data.get("amount")

    order = client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return order


# ---------------- PAYMENT SUCCESS EMAIL ----------------
@app.post("/payment-success")
async def payment_success(request: Request):
    data = await request.json()

    email = data.get("email")
    amount = data.get("amount")

    try:
        msg = MIMEText(f"""
Payment Successful 🎉

Amount: ₹{amount}

Thank you for shopping with us 🛒
""")

        msg["Subject"] = "Payment Successful - SuperMart"
        msg["From"] = EMAIL_USER
        msg["To"] = "amanr835222@gmail.com"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("amanr835222@gmail.com","yxruhdchrosrkzbc" )

        server.send_message(msg)
        server.quit()

        return {"message": "Email sent ✅"}

    except Exception as e:
        return {"error": str(e)}
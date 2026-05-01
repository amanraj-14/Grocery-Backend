from sqlalchemy.orm import Session
from models import Product
from database import SessionLocal

def seed_products(db: Session):
    products = [
        {"name": "Apple", "price": 50, "category": "Fruit", "image": "apple.jpg"},
        {"name": "Banana", "price": 30, "category": "Fruit", "image": "banana.jpg"},
        {"name": "Milk", "price": 60, "category": "Dairy", "image": "milk.jpg"},
        {"name": "Bread", "price": 40, "category": "Bakery", "image": "bread.jpg"},
        {"name": "Eggs", "price": 70, "category": "Dairy", "image": "eggs.jpg"},
        {"name": "Rice", "price": 100, "category": "Grains", "image": "rice.jpg"},
        {"name": "Wheat Flour", "price": 120, "category": "Grains", "image": "flour.jpg"},
        {"name": "Tomato", "price": 25, "category": "Vegetable", "image": "tomato.jpg"},
        {"name": "Potato", "price": 20, "category": "Vegetable", "image": "potato.jpg"},
        {"name": "Onion", "price": 30, "category": "Vegetable", "image": "onion.jpg"},
        {"name": "Chicken", "price": 200, "category": "Meat", "image": "chicken.jpg"},
        {"name": "Fish", "price": 250, "category": "Meat", "image": "fish.jpg"},
        {"name": "Butter", "price": 90, "category": "Dairy", "image": "butter.jpg"},
        {"name": "Cheese", "price": 150, "category": "Dairy", "image": "cheese.jpg"},
        {"name": "Yogurt", "price": 50, "category": "Dairy", "image": "yogurt.jpg"},
        {"name": "Orange", "price": 60, "category": "Fruit", "image": "orange.jpg"},
        {"name": "Mango", "price": 80, "category": "Fruit", "image": "mango.jpg"},
        {"name": "Pineapple", "price": 90, "category": "Fruit", "image": "pineapple.jpg"},
        {"name": "Cabbage", "price": 35, "category": "Vegetable", "image": "cabbage.jpg"},
        {"name": "Carrot", "price": 40, "category": "Vegetable", "image": "carrot.jpg"},
        {"name": "Spinach", "price": 20, "category": "Vegetable", "image": "spinach.jpg"},
        {"name": "Salt", "price": 15, "category": "Essentials", "image": "salt.jpg"},
        {"name": "Sugar", "price": 45, "category": "Essentials", "image": "sugar.jpg"},
        {"name": "Oil", "price": 120, "category": "Essentials", "image": "oil.jpg"},
        {"name": "Tea", "price": 180, "category": "Beverages", "image": "tea.jpg"},
        {"name": "Coffee", "price": 220, "category": "Beverages", "image": "coffee.jpg"},
        {"name": "Biscuits", "price": 25, "category": "Snacks", "image": "biscuits.jpg"},
        {"name": "Chips", "price": 30, "category": "Snacks", "image": "chips.jpg"},
        {"name": "Juice", "price": 70, "category": "Beverages", "image": "juice.jpg"},
        {"name": "Soft Drink", "price": 90, "category": "Beverages", "image": "softdrink.jpg"}
    ]

    for item in products:
        db.add(Product(**item))

    db.commit()
    from database import SessionLocal

if __name__ == "__main__":
    db = SessionLocal()
    seed_products(db)
    db.close()
    print("Data inserted successfully ✅")
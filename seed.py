"""
Seed script to populate the database with sample data
"""
from sqlalchemy.orm import Session
from ecommerce.database import SessionLocal, engine, Base
from ecommerce.models import User, Category, Product
from ecommerce.auth import get_password_hash

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already seeded!")
            return
        
        print("Seeding database...")
        
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True
        )
        db.add(admin)
        
        # Create regular user
        user = User(
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            hashed_password=get_password_hash("password123"),
            is_admin=False,
            is_active=True
        )
        db.add(user)
        
        # Create categories
        categories = [
            Category(name="Electronics", description="Electronic devices and gadgets"),
            Category(name="Clothing", description="Fashion and apparel"),
            Category(name="Books", description="Books and literature"),
            Category(name="Home & Garden", description="Home improvement and garden supplies"),
            Category(name="Sports", description="Sports equipment and accessories"),
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # Create products
        products = [
            # Electronics
            Product(
                name="Laptop Pro 15",
                description="High-performance laptop with 16GB RAM and 512GB SSD",
                price=1299.99,
                stock=50,
                category_id=1,
                image_url="https://example.com/laptop.jpg"
            ),
            Product(
                name="Wireless Mouse",
                description="Ergonomic wireless mouse with precision tracking",
                price=29.99,
                stock=200,
                category_id=1,
                image_url="https://example.com/mouse.jpg"
            ),
            Product(
                name="Smartphone X",
                description="Latest smartphone with 5G connectivity",
                price=899.99,
                stock=100,
                category_id=1,
                image_url="https://example.com/phone.jpg"
            ),
            
            # Clothing
            Product(
                name="Cotton T-Shirt",
                description="Comfortable 100% cotton t-shirt",
                price=19.99,
                stock=500,
                category_id=2,
                image_url="https://example.com/tshirt.jpg"
            ),
            Product(
                name="Denim Jeans",
                description="Classic blue denim jeans",
                price=49.99,
                stock=300,
                category_id=2,
                image_url="https://example.com/jeans.jpg"
            ),
            
            # Books
            Product(
                name="Python Programming Guide",
                description="Comprehensive guide to Python programming",
                price=39.99,
                stock=150,
                category_id=3,
                image_url="https://example.com/python-book.jpg"
            ),
            Product(
                name="Web Development Handbook",
                description="Modern web development techniques and best practices",
                price=44.99,
                stock=120,
                category_id=3,
                image_url="https://example.com/web-book.jpg"
            ),
            
            # Home & Garden
            Product(
                name="Garden Tool Set",
                description="Complete set of essential garden tools",
                price=79.99,
                stock=80,
                category_id=4,
                image_url="https://example.com/tools.jpg"
            ),
            Product(
                name="LED Desk Lamp",
                description="Adjustable LED desk lamp with USB charging",
                price=34.99,
                stock=250,
                category_id=4,
                image_url="https://example.com/lamp.jpg"
            ),
            
            # Sports
            Product(
                name="Yoga Mat",
                description="Non-slip yoga mat with carrying strap",
                price=24.99,
                stock=400,
                category_id=5,
                image_url="https://example.com/yoga-mat.jpg"
            ),
            Product(
                name="Running Shoes",
                description="Lightweight running shoes with cushioned sole",
                price=89.99,
                stock=180,
                category_id=5,
                image_url="https://example.com/shoes.jpg"
            ),
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        print("\nTest Credentials:")
        print("Admin - Username: admin, Password: admin123")
        print("User - Username: john_doe, Password: password123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

import httpx
import json
import secrets
import string

BASE_URL = "http://localhost:8000"

def generate_random_string(length=8):
    return ''.join(secrets.choice(string.ascii_lowercase) for _ in range(length))

def test_endpoints():
    print("Starting Comprehensive API Testing...")
    
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. Health Check
        print("\nTesting Health Check...")
        resp = client.get("/health")
        print(f"Status: {resp.status_code}, Data: {resp.json()}")
        assert resp.status_code == 200

        # 2. Authentication Testing
        print("\nTesting Authentication...")
        
        # Register new user
        username = f"testuser_{generate_random_string()}"
        email = f"{username}@example.com"
        reg_payload = {
            "username": username,
            "email": email,
            "password": "password123",
            "full_name": "Test User"
        }
        print(f"Registering user: {username}")
        resp = client.post("/auth/register", json=reg_payload)
        print(f"Register Status: {resp.status_code}")
        assert resp.status_code == 201
        
        # Login (Regular User)
        print("Logging in as regular user...")
        login_data = {"username": username, "password": "password123"}
        resp = client.post("/auth/login", data=login_data)
        print(f"Login Status: {resp.status_code}")
        assert resp.status_code == 200
        user_token = resp.json()["access_token"]
        user_headers = {"Authorization": f"Bearer {user_token}"}

        # Login (Admin User - from seed)
        print("Logging in as admin user...")
        admin_login_data = {"username": "admin", "password": "admin123"}
        resp = client.post("/auth/login", data=admin_login_data)
        print(f"Admin Login Status: {resp.status_code}")
        assert resp.status_code == 200
        admin_token = resp.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Get Me
        print("Fetching /auth/me for user...")
        resp = client.get("/auth/me", headers=user_headers)
        print(f"Me Status: {resp.status_code}, User: {resp.json()['username']}")
        assert resp.status_code == 200

        # 3. Categories Testing
        print("\nTesting Categories...")
        
        # Create Category (Admin)
        cat_name = f"TestCat_{generate_random_string()}"
        resp = client.post("/categories/", json={"name": cat_name, "description": "Testing category"}, headers=admin_headers)
        print(f"Create Category Status: {resp.status_code}")
        assert resp.status_code == 201
        category_id = resp.json()["id"]

        # Get All Categories
        resp = client.get("/categories/")
        print(f"Get All Categories Status: {resp.status_code}, Count: {len(resp.json())}")
        assert resp.status_code == 200

        # 4. Products Testing
        print("\nTesting Products...")
        
        # Create Product (Admin)
        prod_payload = {
            "name": f"Test Prod {generate_random_string()}",
            "description": "Testing product description",
            "price": 99.99,
            "stock": 10,
            "category_id": category_id
        }
        resp = client.post("/products/", json=prod_payload, headers=admin_headers)
        print(f"Create Product Status: {resp.status_code}")
        assert resp.status_code == 201
        product_id = resp.json()["id"]

        # Get Products (Search & Filter)
        resp = client.get(f"/products/?search=Test&category_id={category_id}")
        print(f"Search Products Status: {resp.status_code}, Count: {len(resp.json())}")
        assert resp.status_code == 200

        # 5. Cart Testing
        print("\nTesting Shopping Cart...")
        
        # Add to Cart
        resp = client.post("/cart/items", json={"product_id": product_id, "quantity": 2}, headers=user_headers)
        print(f"Add to Cart Status: {resp.status_code}")
        assert resp.status_code == 201
        cart_item_id = resp.json()["id"]

        # Get Cart
        resp = client.get("/cart/", headers=user_headers)
        print(f"Get Cart Status: {resp.status_code}, Total: {resp.json()['total']}")
        assert resp.status_code == 200

        # Update Cart Item
        resp = client.put(f"/cart/items/{cart_item_id}", json={"quantity": 3}, headers=user_headers)
        print(f"Update Cart Item Status: {resp.status_code}, New Quantity: {resp.json()['quantity']}")
        assert resp.status_code == 200

        # 6. Orders Testing
        print("\nTesting Orders...")
        
        # Create Order
        resp = client.post("/orders/", json={"shipping_address": "456 Test Lane, QA City"}, headers=user_headers)
        print(f"Create Order Status: {resp.status_code}, Order ID: {resp.json()['id']}")
        assert resp.status_code == 201
        order_id = resp.json()["id"]

        # Get User Orders
        resp = client.get("/orders/", headers=user_headers)
        print(f"Get User Orders Status: {resp.status_code}, Count: {len(resp.json())}")
        assert resp.status_code == 200

        # Get All Orders (Admin)
        resp = client.get("/orders/all", headers=admin_headers)
        print(f"Get All Orders (Admin) Status: {resp.status_code}, Count: {len(resp.json())}")
        assert resp.status_code == 200

        # Update Order Status (Admin)
        resp = client.put(f"/orders/{order_id}/status", json={"status": "processing"}, headers=admin_headers)
        print(f"Update Order Status Status: {resp.status_code}, New Status: {resp.json()['status']}")
        assert resp.status_code == 200

        # 7. Cleanup (Optional but good for testing delete)
        print("\nTesting Deletion and Cleanup...")
        
        # Clear Cart (even though it empties on order, let's test the endpoint)
        resp = client.delete("/cart/clear", headers=user_headers)
        print(f"Clear Cart Status: {resp.status_code}")
        assert resp.status_code == 204

        # Delete Product (Admin)
        resp = client.delete(f"/products/{product_id}", headers=admin_headers)
        print(f"Delete Product Status: {resp.status_code}")
        assert resp.status_code == 204

        # Delete Category (Admin)
        resp = client.delete(f"/categories/{category_id}", headers=admin_headers)
        print(f"Delete Category Status: {resp.status_code}")
        assert resp.status_code == 204

    print("\nAll Tests Passed Successfully!")

if __name__ == "__main__":
    try:
        test_endpoints()
    except Exception as e:
        print(f"\nTest Failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Error Content: {e.response.text}")

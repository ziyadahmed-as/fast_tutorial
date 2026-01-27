# E-Commerce API with FastAPI

A simple yet comprehensive e-commerce REST API built with FastAPI, featuring user authentication, product management, shopping cart, and order processing.

## Features

- 🔐 **User Authentication** - JWT-based authentication with registration and login
- 📦 **Product Management** - CRUD operations for products with categories
- 🛒 **Shopping Cart** - Add, update, and remove items from cart
- 📋 **Order Management** - Create orders from cart, track order status
- 👥 **User Roles** - Admin and regular user roles with different permissions
- 🔍 **Search & Filter** - Search products by name/description and filter by category
- 📊 **Stock Management** - Automatic stock tracking and validation

## Project Structure

```
FastAPI/
├── ecommerce/
│   ├── __init__.py
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py   # Authentication endpoints
│       ├── category_routes.py
│       ├── product_routes.py
│       ├── cart_routes.py
│       └── order_routes.py
├── app.py                   # Main application
├── seed.py                  # Database seeding script
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- XAMPP with MySQL running
- pip (Python package manager)

### Setup Steps

1. **Start XAMPP MySQL:**
   - Open XAMPP Control Panel
   - Start the MySQL service
   - Ensure it's running on port 3306 (default)

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

1. **Create the MySQL database:**

   **Option A - Using Python script (Recommended):**

   ```bash
   python setup_database.py
   ```

   **Option B - Using phpMyAdmin:**
   - Open <http://localhost/phpmyadmin>
   - Click "SQL" tab
   - Copy and paste the contents of `create_database.sql`
   - Click "Go"

   **Option C - Using MySQL command line:**

   ```bash
   mysql -u root -p < create_database.sql
   ```

2. **Configure database connection (Optional):**

   The application uses default XAMPP MySQL settings:
   - Host: localhost
   - Port: 3306
   - User: root
   - Password: (empty)
   - Database: ecommerce_db

   To customize, create a `.env` file (copy from `.env.example`):

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` with your settings.

3. **Seed the database with sample data:**

```bash
python seed.py
```

1. **Run the application:**

```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## Test Credentials

After running the seed script, you can use these credentials:

**Admin User:**

- Username: `admin`
- Password: `admin123`

**Regular User:**

- Username: `john_doe`
- Password: `password123`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user information

### Categories

- `GET /categories/` - Get all categories
- `GET /categories/{id}` - Get category by ID
- `POST /categories/` - Create category (Admin only)
- `PUT /categories/{id}` - Update category (Admin only)
- `DELETE /categories/{id}` - Delete category (Admin only)

### Products

- `GET /products/` - Get all products (with search & filter)
- `GET /products/{id}` - Get product by ID
- `POST /products/` - Create product (Admin only)
- `PUT /products/{id}` - Update product (Admin only)
- `DELETE /products/{id}` - Delete product (Admin only)

### Shopping Cart

- `GET /cart/` - Get user's cart
- `POST /cart/items` - Add item to cart
- `PUT /cart/items/{id}` - Update cart item quantity
- `DELETE /cart/items/{id}` - Remove item from cart
- `DELETE /cart/clear` - Clear entire cart

### Orders

- `GET /orders/` - Get user's orders
- `GET /orders/all` - Get all orders (Admin only)
- `GET /orders/{id}` - Get order by ID
- `POST /orders/` - Create order from cart
- `PUT /orders/{id}/status` - Update order status (Admin only)
- `DELETE /orders/{id}` - Cancel order (if pending)

## Usage Examples

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### 3. Get products (with authentication)

```bash
curl -X GET "http://localhost:8000/products/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Add item to cart

```bash
curl -X POST "http://localhost:8000/cart/items" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### 5. Create order

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "shipping_address": "123 Main St, City, Country"
  }'
```

## Database Schema

The application uses MySQL (via XAMPP) with the following main tables:

- **users** - User accounts and authentication
- **categories** - Product categories
- **products** - Product catalog
- **cart_items** - Shopping cart items
- **orders** - Customer orders
- **order_items** - Items within orders

Tables are automatically created by SQLAlchemy when you first run the application.

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Role-based access control (Admin/User)
- Protected endpoints requiring authentication
- Input validation using Pydantic

## Development

To modify the application:

1. Update models in `ecommerce/models.py`
2. Update schemas in `ecommerce/schemas.py`
3. Add/modify routes in `ecommerce/routes/`
4. The database will be automatically created/updated

## Production Considerations

Before deploying to production:

1. Change the `SECRET_KEY` in `ecommerce/auth.py`
2. Use a production database (PostgreSQL, MySQL)
3. Configure proper CORS origins in `app.py`
4. Enable HTTPS
5. Set up proper logging
6. Use environment variables for configuration

## License

MIT License

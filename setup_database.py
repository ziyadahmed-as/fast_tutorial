"""
Setup script to create the MySQL database
Run this before running the application for the first time
"""
import pymysql
import sys

# XAMPP MySQL default configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # XAMPP default has no password
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
DATABASE_NAME = "ecommerce_db"

def create_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{DATABASE_NAME}' created successfully!")
        
        # Show databases to confirm
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        if any(DATABASE_NAME in db for db in databases):
            print(f"✅ Confirmed: Database '{DATABASE_NAME}' exists")
        
        cursor.close()
        connection.close()
        
        print("\n📝 Next steps:")
        print("1. Run: python seed.py (to populate the database with sample data)")
        print("2. Run: python app.py (to start the application)")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error creating database: {e}")
        print("\n💡 Make sure:")
        print("1. XAMPP MySQL is running")
        print("2. MySQL credentials are correct (default: user='root', password='')")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Creating MySQL database for E-Commerce application...")
    print(f"📍 Host: {MYSQL_HOST}:{MYSQL_PORT}")
    print(f"👤 User: {MYSQL_USER}")
    print(f"🗄️  Database: {DATABASE_NAME}\n")
    
    success = create_database()
    sys.exit(0 if success else 1)

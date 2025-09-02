# setup_database.py
import sqlite3
import json

print("Starting database setup...")

# Connect to the database (creates the file if it doesn't exist)
connection = sqlite3.connect('customer_service.db')
cursor = connection.cursor()

# Use 'DROP TABLE' for a clean slate during development.
# In a real application, you'd use a more robust migration system.
cursor.execute('DROP TABLE IF EXISTS purchase_items')
cursor.execute('DROP TABLE IF EXISTS products')
cursor.execute('DROP TABLE IF EXISTS purchases')
cursor.execute('DROP TABLE IF EXISTS customers')


# 1. Create the 'customers' table with all flattened fields
print("Creating 'customers' table...")
cursor.execute('''
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    account_number TEXT NOT NULL,
    customer_first_name TEXT NOT NULL,
    customer_last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone_number TEXT,
    customer_start_date TEXT,
    years_as_customer INTEGER,
    billing_address_street TEXT,
    billing_address_city TEXT,
    billing_address_state TEXT,
    billing_address_zip TEXT,
    loyalty_points INTEGER,
    preferred_store TEXT,
    comm_pref_email INTEGER,
    comm_pref_sms INTEGER,
    comm_pref_push INTEGER,
    garden_type TEXT,
    garden_size TEXT,
    garden_sun_exposure TEXT,
    garden_soil_type TEXT,
    garden_interests TEXT,
    scheduled_appointments TEXT
)
''')

# 2. Create a 'products' table to store unique product information
print("Creating 'products' table...")
cursor.execute('''
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# 3. Create the 'purchases' table
print("Creating 'purchases' table...")
cursor.execute('''
CREATE TABLE purchases (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
)
''')

# 4. Create a linking table for items within a purchase (Many-to-Many relationship)
print("Creating 'purchase_items' table...")
cursor.execute('''
CREATE TABLE purchase_items (
    purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_id INTEGER NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchases (purchase_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

# --- Insert the Sample Data ---
print("Inserting sample data...")
try:
    # Insert customer data
    cursor.execute('''
    INSERT INTO customers (customer_id, account_number, customer_first_name, customer_last_name, email, phone_number, customer_start_date, years_as_customer, billing_address_street, billing_address_city, billing_address_state, billing_address_zip, loyalty_points, preferred_store, comm_pref_email, comm_pref_sms, comm_pref_push, garden_type, garden_size, garden_sun_exposure, garden_soil_type, garden_interests, scheduled_appointments)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "CUST001", "ACC12345", "John", "Smith", "john.smith@email.com", "555-0123",
        "2020-05-01", 4, "123 Garden Lane", "Springfield", "IL", "62701",
        250, "Springfield Garden Center", 1, 0, 1, "Vegetable Garden", "Medium",
        "Full Sun", "Loamy", "Organic Gardening,Composting,Herb Growing",
        json.dumps({})
    ))

    # Insert unique products (use IGNORE to avoid errors on duplicates)
    products_to_insert = [
        ('fert-111', 'All-Purpose Fertilizer'),
        ('trowel-222', 'Gardening Trowel'),
        ('seeds-333', 'Tomato Seeds (Variety Pack)'),
        ('pots-444', 'Terracotta Pots (6-inch)'),
        ('gloves-555', 'Gardening Gloves (Leather)'),
        ('pruner-666', 'Pruning Shears')
    ]
    cursor.executemany('INSERT OR IGNORE INTO products (product_id, name) VALUES (?, ?)', products_to_insert)

    # Insert purchases and their related items
    sample_purchases = [
        {"date": "2023-03-05", "total": 35.98, "items": [("fert-111", 1), ("trowel-222", 1)]},
        {"date": "2023-07-12", "total": 42.50, "items": [("seeds-333", 2), ("pots-444", 4)]},
        {"date": "2024-01-20", "total": 55.25, "items": [("gloves-555", 1), ("pruner-666", 1)]}
    ]

    for purchase in sample_purchases:
        cursor.execute('INSERT INTO purchases (customer_id, date, total_amount) VALUES (?, ?, ?)',
                       ("CUST001", purchase["date"], purchase["total"]))
        purchase_id = cursor.lastrowid  # Get the ID of the purchase we just inserted
        for product_id, quantity in purchase["items"]:
            cursor.execute('INSERT INTO purchase_items (purchase_id, product_id, quantity) VALUES (?, ?, ?)',
                           (purchase_id, product_id, quantity))

    # Commit the changes to the database
    connection.commit()
    print("Database 'customer_service.db' set up successfully with new schema and sample data.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    connection.rollback() # Roll back changes if anything goes wrong

finally:
    # Close the connection
    connection.close()
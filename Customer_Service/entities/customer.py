import sqlite3
import json
from typing import List, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    """
    Represents the address of a customer.
    """
    street: str
    city: str
    state: str
    zip: str
    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    """
    Represents a product in a customer's purchase history.
    """
    product_id: str
    name: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class Purchase(BaseModel):
    """
    Represents a customer's purchase.
    """
    date: str
    items: List[Product]
    total_amount: float
    model_config = ConfigDict(from_attributes=True)


class CommunicationPreferences(BaseModel):
    """
    Represents a customer's communication preferences.
    """
    email: bool = True
    sms: bool = True
    push_notifications: bool = True
    model_config = ConfigDict(from_attributes=True)


class GardenProfile(BaseModel):
    """
    Represents a customer's garden profile.
    """
    type: str
    size: str
    sun_exposure: str
    soil_type: str
    interests: List[str]
    model_config = ConfigDict(from_attributes=True)


class Customer(BaseModel):
    """
    Represents a customer with all their relevant details.
    """
    account_number: str
    customer_id: str
    customer_first_name: str
    customer_last_name: str
    email: str
    phone_number: Optional[str] = None
    customer_start_date: str
    years_as_customer: int
    billing_address: Address
    purchase_history: List[Purchase] = Field(default_factory=list)
    loyalty_points: int = 0
    preferred_store: str
    communication_preferences: CommunicationPreferences
    garden_profile: Optional[GardenProfile] = None
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def get_customer(customer_id: str)-> Optional['Customer']:
        """
        Fetches customer data from the SQLite database and returns a Customer object.
        """
        conn = None
        try:
            conn = sqlite3.connect('customer_service.db')
            conn.row_factory = sqlite3.Row  # Allows accessing columns by name
            cursor = conn.cursor()

            # 1. Fetch main customer details from the flattened table
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
            customer_row = cursor.fetchone()

            if customer_row is None:
                print(f"Customer with ID {customer_id} not found.")
                return None

            # 2. Reconstruct nested Pydantic models from flattened columns
            billing_address = Address(
                street=customer_row['billing_address_street'],
                city=customer_row['billing_address_city'],
                state=customer_row['billing_address_state'],
                zip=customer_row['billing_address_zip']
            )

            comm_prefs = CommunicationPreferences(
                email=bool(customer_row['comm_pref_email']),
                sms=bool(customer_row['comm_pref_sms']),
                push_notifications=bool(customer_row['comm_pref_push'])
            )

            garden_profile = None
            if customer_row['garden_type']:
                garden_profile = GardenProfile(
                    type=customer_row['garden_type'],
                    size=customer_row['garden_size'],
                    sun_exposure=customer_row['garden_sun_exposure'],
                    soil_type=customer_row['garden_soil_type'],
                    interests=json.loads(customer_row['garden_interests'])
                )

            # 3. Fetch purchase history from related tables
            purchase_history = []
            cursor.execute("SELECT * FROM purchases WHERE customer_id = ?", (customer_id,))
            purchase_rows = cursor.fetchall()

            for purchase_row in purchase_rows:
                cursor.execute("""
                               SELECT pi.product_id, pi.quantity, p.name
                               FROM purchase_items pi
                                        JOIN products p ON pi.product_id = p.product_id
                               WHERE pi.purchase_id = ?
                               """, (purchase_row['purchase_id'],))
                item_rows = cursor.fetchall()

                items = [Product(product_id=item['product_id'], name=item['name'], quantity=item['quantity']) for item
                         in item_rows]

                purchase = Purchase(
                    date=purchase_row['date'],
                    items=items,
                    total_amount=purchase_row['total_amount']
                )
                purchase_history.append(purchase)

            # 4. Create the final Customer object
            customer_data = dict(customer_row)
            customer_data['billing_address'] = billing_address
            customer_data['purchase_history'] = purchase_history
            customer_data['communication_preferences'] = comm_prefs
            customer_data['garden_profile'] = garden_profile

            return cls(**customer_data)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()


# Example of how to use the new method
if __name__ == '__main__':
    # Make sure to run your setup_database.py script first to create the db file
    db_file = "customer_service.db"

    # Assuming there's a customer with ID 'CUST001' in your db
    fetched_customer = Customer.get_customer_from_db(db_file, "CUST001")

    if fetched_customer:
        print("Successfully fetched customer details from the database:")
        print(fetched_customer.model_dump_json(indent=2))
    else:
        print("Could not fetch customer.")
from datetime import datetime, timedelta
import uuid
from typing import Dict, List
import logging

def send_call_companion_link(phone_number: str) -> Dict:
    """
    Sends a link to the user's phone number to start a video session.

    :param phone_number: The phone number to send the link to.
    :return: dict: A dictionary with the status and message.
    """
    logging.info(f"Sending call companion link to {phone_number}")
    return {"status": "success", "message": f"Call companion link sent successfully to {phone_number}."}


def approve_discount(discount_type: str, value: float, reason: str) -> Dict:
    """
    Approves the flat rate or percentage discount requested by the user.

    :param discount_type (str): The type of discount to approve, either "flat" or "percentage".
    :param value (float): The value of the discount.
    :param reason (str): The reason for approving the discount.
    :return: dict: A dictionary with the status of the approval and reject reason (if any).
    """

    if value > 10:
        logging.info(f"Denying {discount_type} discount of {value}")
        return {"status": "rejected",
                "message": f"Discount too large. Must be 10 or less."}

    logging.info(f"Approving {discount_type} discount of {value} because {reason}")
    return {"status": "ok"}


def sync_ask_for_approval(discount_type: str, value: float, reason: str) -> Dict:
    """
    Asks the manager for approval for a discount .

    :param discount_type: The type of discount, either "percentage" or "flat"
    :param value: The value of the discount
    :param reason: The reason for the discount.
    :return: dict: A dictionary with the status of the approval and reject reason (if any).
    """

    logging.info(f"Requesting manager approval for {discount_type} discount of {value} because {reason}")

    return {"status": "approved"}


def update_salesforce_crm(customer_id: str, details: dict) -> dict:
    """
    Updates the salesforce CRM with the customer details.

    :param customer_id: The ID of the customer to update.
    :param details: A dictionary of the customer details to update in SalesForce.
    :return: dict: A dictionary with the status and message.

    Example:
        >>> update_salesforce_crm(customer_id='123', details={
            'appointment_date': '2024-07-25',
            'appointment_time': '9-12',
            'services': 'Planting',
            'discount': '15% off planting',
            'qr_code': '10% off next in-store purchase'})
        {'status': 'success', 'message': 'Salesforce record updated  successfully for customer 123.'}

    """
    logging.info(f"Updating salesforce CRM for customer {customer_id} with details {details}")
    return {"status": "success", "message": f"Salesforce record updated successfully for customer {customer_id}."}


def access_cart_information(customer_id: str) -> dict:
    """
    Cart information of the provided customer, who is identified by customer_id.

    :param customer_id: The ID of the customer.
    :return: dict: A dictionary representing the cart contents.

    Example:
        >>> access_cart_information(customer_id='123')
        {'items': [{'product_id': 'soil-123', 'name': 'Standard Potting Soil', 'quantity': 1}, {'product_id': 'fert-456', 'name': 'General Purpose Fertilizer', 'quantity': 1}], 'subtotal': 25.98}
    """

    logging.info(f"Accessing cart information for customer ID: {customer_id}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.
    mock_cart = {
        "items": [
            {
                "product_id": "soil-123",
                "name": "Standard Potting Soil",
                "quantity": 1
            },
            {
                "product_id": "fert-456",
                "name": "General Purpose Fertilizer",
                "quantity": 1
            }
        ],
        "subtotal": 25.98
    }

    return mock_cart


def modify_cart(
        customer_id: str,
        items_to_add: List[dict],
        items_to_remove: List[dict]
) -> dict:
    """
    Modifies the user's shopping card by adding and/or removing items.

    :param customer_id: The ID of the customer.
    :param items_to_add:  A list of dictionaries representing the items to add to the cart. Each item will have 'product_id' and 'quantity'.
    :param items_to_remove: A list of dictionaries representing the items to remove from the cart. Each item will have 'product_id'.
    :return: A dictionary indicating the status of the card modification.

    Example:
        >>> modify_cart(customer_id='123', items_to_add=[{'product_id': 'soil-456', 'quantity': 1}, {'product_id': 'fert-789', 'quantity': 1}], items_to_remove=[{'product_id': 'fert-112'}])
        {'status': 'success', 'message': 'Cart updated successfully.', 'items_added': True, 'items_removed': True}
    """
    # MOCK API Response: Replacing the actual API call with hard-coded data for now.

    return {
        "status": "success",
        "message": "Cart updated successfully.",
        "items_added": True,
        "items_removed": True
    }


def get_product_recommendations(plant_type: str, customer_id: str) -> dict:
    """
    Provides product recommendations based on the type of plant.

    :param plant_type: The type of plant (e.g., 'Petunias', 'Sun-loving annuals', etc.)
    :param customer_id: The ID of the customer for personalized recommendations.
    :return:  A dictionary representing the recommended products. Example:
        {'recommendations': [
            {'product_id': 'soil-456', 'name': 'Bloom Booster Potting Mix', 'description': '...'},
            {'product_id': 'fert-789', 'name': 'Flower Power Fertilizer', 'description': '...'}
        ]}
    """

    logging.info(f"Getting product recommendations for plant type: {plant_type} for customer ID: {customer_id}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.

    if plant_type.lower() == "petunias":
        recommendations = {
            "recommendations": [
                {
                    "product_id": "soil-456",
                    "name": "Bloom Booster Potting Mix",
                    "description": "Provides extra nutrients that Petunias love.",
                },
                {
                    "product_id": "fert-789",
                    "name": "Flower Power Fertilizer",
                    "description": "Specifically formulated for flowering annuals.",
                },
            ]
        }
    else:
        recommendations = {
            "recommendations": [
                {
                    "product_id": "soil-123",
                    "name": "Standard Potting Soil",
                    "description": "A good all-purpose potting soil.",
                },
                {
                    "product_id": "fert-456",
                    "name": "General Purpose Fertilizer",
                    "description": "Suitable for a wide variety of plants.",
                },
            ]
        }
    return recommendations


def check_product_availability(product_id: str, store_id: str) -> dict:
    """
    Checks the availability of a product at a specific store (or for pickup).

    :param product_id: The ID of the product to check.
    :param store_id: The ID of the store (or 'pickup' for pickup availability.
    :return: A dictionary indicating the availability of the product. Example:
        {'available': True, 'quantity': 5, 'store': 'Main Store'}

    Example:
        >>> check_product_availability(product_id='soil-456', store_id='pickup')
        {'available': True, 'quantity': 10, 'store': 'pickup'}
    """

    logging.info(f"Checking availability of product ID: {product_id} at store ID: {store_id}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.

    return {"available": True, "quantity": 10, "store": store_id}


def schedule_planting_service(
        customer_id: str,
        date: str,
        time_range: str,
        details: str
) -> dict:
    """
    Schedules a planting service appointment for the customer.
    :param customer_id: The ID of the customer.
    :param date: The desired date (YYYY-MM-DD).
    :param time_range: The desired time range (e.g., "9-12").
    :param details: Any additional details for the service. (e.g., "Planting Petunias")
    :return: A dictionary indicating the status of the service scheduling. Example:
        {'status': 'success', 'appointment_id': '12345', 'date': '2024-07-29', 'time': '9:00 AM - 12:00 PM'}
    """

    logging.info(f"Scheduling planting service for customer ID: {customer_id} on date: {date}, time range: {time_range}, details: {details}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.

    start_time_str = time_range.split("-")[0].strip()

    confirmation_time_str = (f"{date} {start_time_str}:00")

    return {
        "status": "success",
        "appointment_id": str(uuid.uuid4()),
        "date": date,
        "time": time_range,
        "confirmation_time": confirmation_time_str
    }


def get_available_planting_times(date: str) -> list:
    """
    Retrieves available planting service time slots for a specific date.

    :param date: The date to check (YYYY-MM-DD).
    :return:  A list of available time slots.

    Example:
        >>> get_available_planting_times(date='2024-07-29')
        ['9-12', '13-16']
    """

    logging.info(f"Getting available planting times for date: {date}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.
    # Generate some mock time slots, ensuring they're in the correct format:
    return ['9-12', '13-16']


def send_care_instructions(
        customer_id: str,
        plant_type: str,
        delivery_method: str
) -> dict:
    """
    Sends an email or SMS with instructions on how to take care of a specific plant type.

    :param customer_id: The ID of the customer.
    :param plant_type: The type of plant to care for.
    :param delivery_method: The method of delivery, either "email" or "sms".
    :return: A dictionary indicating the status of the instruction delivery.

    Example:
        >>> send_care_instructions(customer_id='123', plant_type='Petunias', delivery_method='email')
        {'status': 'success', 'message': 'Care instructions for Petunias sent via email.'}
    """

    logging.info(f"Sending care instructions for plant type: {plant_type} to customer ID: {customer_id} via {delivery_method}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.

    return {
        "status": "success",
        "message": f"Care instructions for {plant_type} sent via {delivery_method}."
    }


def generate_qr_code(
        customer_id: str,
        discount_value: float,
        discount_type: str,
        expiration_date: str
):
    """
    Generates a QR code for the discount.

    :param customer_id: The ID of the customer.
    :param discount_value:  The value of the discount (e.g., 10 for 10%)
    :param discount_type:  The type of discount (e.g., "percentage" or "fixed")
    :param expiration_date:  Number of days until the QR code expires
    :return: A dictionary containing  the QR code data (or a link to it). Example:
        {'status': 'success', 'qr_code_data': '...', 'expiration_date': '2024-08-28'}

    Example:
        >>> generate_qr_code(customer_id='123', discount_value=10.0, discount_type='percentage', expiration_days=30)
        {'status': 'success', 'qr_code_data': 'MOCK_QR_CODE_DATA', 'expiration_date': '2024-08-24'}
    """

    # Guardrails to validate the amount of discount that is acceptable for auto-approved discounts.

    if discount_type == "percentage":
        if discount_value > 10:
            return {
                "status": "error",
                "error_message": "Discount percentage is too high. It must be 10% or less."}
    if discount_type == "fixed" and discount_value > 20:
        return {
            "status": "error",
            "error_message": "Discount value is too high. It must be 20 or less."}

    logging.info(f"Generating QR code for customer ID: {customer_id}, discount value: {discount_value}, discount type: {discount_type}, expiration date: {expiration_date}")

    # MOCK API Response: Replacing the actual API call with hard-coded data for now.

    expiration_date = (datetime.now() + datetime.timedelta(days=expiration_date)).strftime("%Y-%m-%d")

    return {
        "status": "success",
        "qr_code_data": "MOCK_QR_CODE_DATA",
        "expiration_date": expiration_date
    }
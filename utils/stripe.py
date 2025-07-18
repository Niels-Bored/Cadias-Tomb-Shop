import stripe
import requests

from django.conf import settings

from shop.models import Venta


def get_stripe_link(product_name: str, total: float,
                    description: str, email: str, sale_id: str, back_page:str) -> dict:
    """ Send data to stripe api and return stripe url

    Args:
        product_name (str): product
        total (float): order total
        description (str): order description
        email (str): user email
        sale_id (str): sale id from models
        back_page: page to return in case sale goes wrong
        
    Returns:
        str: stripe checkout link
    """
    
    products = {}
    products[product_name] = {
        "amount": 1,
        "image_url": "https://d1w82usnq70pt2.cloudfront.net/wp-content/uploads/2020/11/Salamanders_Aggressor.png",
        "price": total,
        "description": description
    }
    
    request_json = {
        "user": settings.STRIPE_API_USER,
        "url": f"{settings.HOST}{back_page}",
        "url_success": f"{settings.HOST}/sale-done/{sale_id}",
        "products": products,
        "email": email,
        "currency": "mxn"
    }
    
    res = requests.post(settings.STRIPE_API_HOST, json=request_json)
    res.raise_for_status()
    res_data = res.json()
    
    return res_data["stripe_url"]


def get_stripe_link_sale(sale: Venta):
    """ Send data to stripe api and return stripe url
        using venta object
        
    Args:
        sale (Venta): sale object
        
    Returns:
        str: stripe checkout link
    """
    
    product_name = f"Tracker {sale.set.name} {sale.colors_num.num} colors"
    description = ""
    description += f"Set: {sale.set.name} | "
    description += f"Colors: {sale.colors_num.num} | "
    description += f"Client Email: {sale.user.email} | "
    description += f"Client Full Name: {sale.full_name} | "
    
    stripe_link = get_stripe_link(
        product_name=product_name,
        total=sale.total,
        description=description,
        email=sale.user.email,
        sale_id=sale.id
    )
    
    return stripe_link


def update_transaction_link(sale: Venta) -> bool:
    """ Get last sale of specific amount and client
    
    Args:
        sale (Venta): venta object
        
    Returns:
        bool: True if payment found, False otherwise
    """
    
    payment_found = False
    
    # Set stripe api key
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    # Get last payments
    charges = stripe.Charge.list(status="succeeded", limit=100)
    if not charges['data']:
        sale.stripe_link = "No payments found in this stripe account"
    
    # Get client payments
    client_charges = []
    for charge in charges['data']:
        if charge['billing_details']['email'] == sale.user.email:
            print(charge['billing_details']['email'], sale.user.email)
            client_charges.append(charge)
        
    # Filter payments by amount
    for charge in client_charges:
        if charge['amount'] == sale.total * 100:
            payment_id = charge['id']
            sale.stripe_link = f"https://dashboard.stripe.com/payments/{payment_id}"
            payment_found = True
            
    # Return error
    if not payment_found:
        sale.stripe_link = "No payment found with this amount for this client"
   
    # Add staus and save sale
    """ if payment_found:
        status = SaleStatus.objects.get(value="Paid")
    else:
        status = SaleStatus.objects.get(value="Payment Error")
    sale.status = status
    sale.save() """
    
    return payment_found
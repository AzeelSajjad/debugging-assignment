from discounts import apply_discounts
from validators import find_customer_by_id, find_product_by_id, validate_order
from inventory import reserve_inventory
from data import get_products, get_customers, get_orders, get_tax_rates # to test

def calculate_subtotal(order, products):
    subtotal = 0

    for item in order["items"]:
        product = find_product_by_id(products, item["product_id"])
        if product is None:
            continue

        subtotal += product["price"] * item["quantity"] #change '+' into '*' because  the subtotal should be price times quantity not plus.

    return round(subtotal, 2)


def calculate_tax(customer, discounted_subtotal, tax_rates):
    state = customer.get("state", "NJ")
    rate = tax_rates.get(state, 0.07)
    return round(discounted_subtotal * rate, 2)


def calculate_shipping(discounted_subtotal):
    if discounted_subtotal > 100:
        return 0
    return 8.99


def process_order(order, products, customers, tax_rates):
    customer = find_customer_by_id(customers, order.get("customer_id"))

    errors = validate_order(order, products, customers)

    subtotal = calculate_subtotal(order, products)
    discounts = apply_discounts(order, customer, products, subtotal)
    tax = calculate_tax(customer, discounts.get("discounted_subtotal"), tax_rates) #this should not be subtotal, it should be the discounted subtotal: subtotal -> discounts.get("discounted_subtotal")
    shipping = calculate_shipping(subtotal)

    total = discounts["discounted_subtotal"] + tax + shipping

    reserve_inventory(products, order)

    return {
        "order_id": order["id"],
        "customer": customer["name"] if customer else "UNKNOWN",
        "valid": len(errors) == 0,
        "errors": errors,
        "subtotal": round(subtotal, 2),
        "discounts": discounts,
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "total": round(total, 2),
    }

# TESTING

#def check(condition, message):
#    if not condition:
#        raise AssertionError(message)
    
#products = get_products()
#customers = get_customers()
#orders = get_orders()
#tax_rates = get_tax_rates()

#subtotal = calculate_subtotal(orders[0], products)
#check(abs(subtotal - 119.97) < 0.001, "Order 1001 subtotal should be 119.97")

#result = process_order(orders[0], products, customers, tax_rates)
#check(result["valid"] is True, "Order 1001 should be valid")
#check(products[0]["stock"] == 10, "Keyboard stock should decrease by 2")
#check(products[1]["stock"] == 3, "Mouse stock should decrease by 1")

"""print(calculate_subtotal({
            "id": 1001,
            "customer_id": "C001",
            "coupon": "SAVE10",
            "items": [
                {"product_id": "P100", "quantity": 2},
                {"product_id": "P101", "quantity": 1},
            ],
        }, [
        {"id": "P100", "name": "Keyboard", "category": "Electronics", "price": 49.99, "stock": 12},
        {"id": "P101", "name": "Mouse", "category": "Electronics", "price": 19.99, "stock": 4},
        {"id": "P102", "name": "Notebook", "category": "Office", "price": 3.50, "stock": 30},
        {"id": "P103", "name": "Pen Pack", "category": "Office", "price": 5.25, "stock": 0},
        {"id": "P104", "name": "Water Bottle", "category": "Fitness", "price": 14.00, "stock": 7},
        {"id": "P105", "name": "Yoga Mat", "category": "Fitness", "price": 22.50, "stock": 2},
    ]))"""
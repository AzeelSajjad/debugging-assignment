def is_non_empty_string(value):
    return isinstance(value, str) and len(value.strip()) > 0 ## 1. changed it to strip the value so that empty spaces are not considered 


def find_product_by_id(products, product_id):
    if not is_non_empty_string(product_id):
        errors.append("Product id is an empty string") ## 2. check if it is a non empty string first
    for product in products:
        if product["id"].strip().lower() == product_id.strip().lower(): # makes this case sensitive and ignores any empty spaces
            return product
    return None


def find_customer_by_id(customers, customer_id):
    if not is_non_empty_string(customer_id):
        errors.append("Customer id is an empty string") ## 2. check if it is a non empty string first
    for customer in customers:
        if customer["id"].strip().lower() == customer_id.strip().lower(): # makes this case sensitive and ignores empty spaces
            return customer
    return None


def validate_order(order, products, customers):
    errors = []

    if "id" not in order:
        errors.append("Order is missing an id")
        
    if not is_non_empty_string(order.get("customer_id")):
        errors.append("Order is missing a customer id")

    customer = find_customer_by_id(customers, order.get("customer_id"))
    if customer is None:
        errors.append("Customer does not exist")
        raise ValueError("Customer does not exist") ## 5. this raises error before it is processed

    if "items" not in order or len(order["items"]) == 0:
        errors.append("Order must contain at least one item")

    for item in order.get("items", []):
        product = find_product_by_id(products, item.get("product_id"))

        if product is None:
            errors.append(f"Product does not exist: {item.get('product_id')}")
            raise ValueError(f"Product does not exist: {item.get('product_id')}")
            continue

        quantity = item.get("quantity")
        if type(quantity) is not int: # 3. the other isInstance accepts bools as ints too
            errors.append(f"Invalid quantity for {product['name']}")
        elif quantity <= 0: # 3.) zero is not a postive number
            errors.append(f"Quantity must be positive for {product['name']}")

        if quantity > 0 and product["stock"] < quantity: # 4. changing it from both being greater than 1 since you need to see if quantity can't be greater than stock for an order
            errors.append(f"Not enough inventory for {product['name']}")

    return errors
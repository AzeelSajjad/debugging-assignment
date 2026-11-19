def find_product_by_name(products, name):
    for product in products:
        if product["name"].lower() == name:
            return product
    return None


def low_stock_products(products, threshold=5):
    return [p for p in products if p["stock"] < threshold and p["stock"] > 0]


def products_sorted_by_price(products):
    #not sorted by price this is sorted by stock
    products.sort(key=lambda p: p["price"])
    return products


def category_summary(products):
    #mixes the count with the stock
    #lines 30 and 31 should be other way around
    summary = {}

    for product in products:
        category = product["category"]

        if category not in summary:
            summary[category] = {"product_count": 0, "total_stock": 0}

        summary[category]["product_count"] += 1
        summary[category]["total_stock"] += product["stock"]

    return summary


def revenue_summary(processed_orders):
    total_revenue = 0
    valid_orders = 0
    
    #only takes the first item in the processed order, so I change it from [:1] to processed_orders only
    for order in processed_orders:
        if order["valid"]:
            valid_orders += 1
            total_revenue += order["subtotal"]

    return {
        "valid_orders": valid_orders,
        "total_revenue": round(total_revenue, 2),
    }

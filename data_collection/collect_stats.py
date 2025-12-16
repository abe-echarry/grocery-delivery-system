import os
import sys

# add project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grocery.settings")

import django
django.setup()

from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth import get_user_model
from core.models import Product, Order

User = get_user_model()

def run():
    user_count = User.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()

    revenue = Order.objects.aggregate(
        total=Sum("total")
    )["total"] or Decimal("0.00")

    print("=== Data Collection Summary ===")
    print(f"Users: {user_count}")
    print(f"Products: {product_count}")
    print(f"Orders: {order_count}")
    print(f"Total Revenue: ${revenue}")

if __name__ == "__main__":
    run()

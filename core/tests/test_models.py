from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Product, Category, Address, Order
from decimal import Decimal

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Produce")


class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )
        self.category = Category.objects.create(name="Produce")

    def test_product_creation(self):
        product = Product.objects.create(
            category=self.category,
            sku="APL001",
            name="Apple",
            price=Decimal("1.99"),
            stock=10
        )
        self.assertEqual(str(product), "Apple (APL001)")
        self.assertTrue(product.is_active)

    def test_address_creation(self):
        address = Address.objects.create(
            user=self.user,
            line1="123 Main St",
            city="Indy",
            state="IN",
            zip="46201"
        )
        self.assertIn("123 Main St", str(address))

    def test_order_creation(self):
        address = Address.objects.create(
            user=self.user,
            line1="123 Main St",
            city="Indy",
            state="IN",
            zip="46201"
        )
        order = Order.objects.create(
            user=self.user,
            address=address,
            total=Decimal("9.99")
        )
        self.assertEqual(order.total, Decimal("9.99"))

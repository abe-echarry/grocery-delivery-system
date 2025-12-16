from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Category, Product, Address, Order, OrderItem

User = get_user_model()


class IntegrationTests(TestCase):
    def setUp(self):
        # customer
        self.user = User.objects.create_user(username="cust", password="pass1234")
        self.client.login(username="cust", password="pass1234")

        self.category = Category.objects.create(name="Produce")
        self.product = Product.objects.create(
            category=self.category,
            sku="APL001",
            name="Apple",
            price=Decimal("1.50"),
            stock=10,
            is_active=True,
        )

    def test_customer_checkout_creates_order_and_items(self):
        # add to cart
        resp = self.client.post(reverse("cart_add", args=[self.product.id]))
        self.assertEqual(resp.status_code, 302)

        # checkout page loads
        resp = self.client.get(reverse("checkout"))
        self.assertEqual(resp.status_code, 200)

        # submit checkout form (match your Address fields)
        resp = self.client.post(reverse("checkout"), data={
            "line1": "123 Main St",
            "city": "Indy",
            "state": "IN",
            "zip": "46201",
        })
        self.assertEqual(resp.status_code, 302)

        # order exists
        order = Order.objects.filter(user=self.user).order_by("-created_at").first()
        self.assertIsNotNone(order)

        # order item exists
        self.assertTrue(OrderItem.objects.filter(order=order, product=self.product).exists())

        # cart cleared (session cart should be empty dict)
        session = self.client.session
        self.assertEqual(session.get("cart", {}), {})

    def test_courier_claim_updates_status(self):
        # create an order for courier to claim
        addr = Address.objects.create(user=self.user, line1="123 Main St", city="Indy", state="IN", zip="46201")
        order = Order.objects.create(user=self.user, address=addr, total=Decimal("3.00"), status="PLACED")

        # create staff courier
        courier = User.objects.create_user(username="courier", password="pass1234", is_staff=True)
        self.client.logout()
        self.client.login(username="courier", password="pass1234")

        # claim (POST)
        resp = self.client.post(reverse("courier_claim", args=[order.id]))
        self.assertEqual(resp.status_code, 302)

        order.refresh_from_db()
        self.assertEqual(order.status, "ASSIGNED")
        self.assertEqual(order.courier, courier)

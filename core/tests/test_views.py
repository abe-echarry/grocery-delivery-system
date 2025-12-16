from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Product, SavedItem, Category


User = get_user_model()


class SavedViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u3", password="pass1234")
        self.client.login(username="u3", password="pass1234")

        self.category = Category.objects.create(name="Produce")
        self.product = Product.objects.create(
            category=self.category,
            sku="BAN001",
            name="Banana",
            price=Decimal("0.99"),
            stock=10,
            is_active=True,
        )


    def test_saved_add_creates_row(self):
        url = reverse("saved_add", args=[self.product.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # redirect
        self.assertTrue(SavedItem.objects.filter(user=self.user, product=self.product).exists())

    def test_saved_remove_deletes_row(self):
        SavedItem.objects.create(user=self.user, product=self.product)

        url = reverse("saved_remove", args=[self.product.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # redirect
        self.assertFalse(SavedItem.objects.filter(user=self.user, product=self.product).exists())

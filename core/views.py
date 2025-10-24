from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.filter(is_active=True).order_by("name")[:24]
    return render(request, "home.html", {"products": products})


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product

#helpers 
def _get_cart(session) -> dict:
    """
    Return a mutable cart dict stored in the session.
    Structure: { "<product_id>": quantity_int }
    """
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart

#actions
def cart_add(request, product_id):
    # add 1 to the item (create if missing)
    cart = _get_cart(request.session)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session.modified = True
    return HttpResponseRedirect(reverse("cart"))

def cart_remove(request, product_id):
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return HttpResponseRedirect(reverse("cart"))

def cart_update(request, product_id):
    # expects POST {qty: int}
    qty = int(request.POST.get("qty", 1))
    cart = _get_cart(request.session)
    pid = str(product_id)
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    request.session.modified = True
    return HttpResponseRedirect(reverse("cart"))

def cart_view(request):
    cart = _get_cart(request.session)
    ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=ids)

    items = []
    total = 0.0
    for p in products:
        qty = cart.get(str(p.id), 0)
        line_total = float(p.price) * qty
        total += line_total
        items.append({"product": p, "qty": qty, "line_total": line_total})

    return render(request, "cart.html", {"items": items, "total": total})

#chekcout + create order
from decimal import Decimal
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from .forms import AddressForm
from .models import Address, Order, OrderItem, Product

def _get_cart(session) -> dict:
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart

def checkout(request):
    """Create/choose address, compute totals, create Order + OrderItems, clear cart."""
    cart = _get_cart(request.session)
    if not cart:
        return redirect("cart")

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Persist (or reuse) address for this user
                address, _ = Address.objects.get_or_create(user=request.user, **form.cleaned_data)

                # Load products currently in cart
                ids = [int(pid) for pid in cart.keys()]
                products = list(Product.objects.filter(id__in=ids, is_active=True))  # only active

                # Build order
                order = Order.objects.create(user=request.user, address=address, total=Decimal("0.00"))
                total = Decimal("0.00")

                # Create items and compute total using *current* prices
                for p in products:
                    qty = int(cart.get(str(p.id), 0))
                    if qty <= 0:
                        continue
                    line = (p.price * qty)
                    OrderItem.objects.create(order=order, product=p, quantity=qty, price_each=p.price)
                    total += line

                order.total = total.quantize(Decimal("0.01"))
                order.save()

                # Clear cart
                request.session["cart"] = {}
                request.session.modified = True

                return redirect("order_success", order_id=order.id)
    else:
        form = AddressForm()

    return render(request, "checkout.html", {"form": form})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})

#view for order lists + detail
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_history(request):
    """Show all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/history.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    """Show a single order with its items."""
    order = Order.objects.get(id=order_id, user=request.user)
    items = order.items.select_related("product")
    return render(request, "orders/detail.html", {"order": order, "items": items})




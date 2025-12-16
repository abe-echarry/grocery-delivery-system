from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Product, SavedItem
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.db.models import Q

def home(request):
    q = request.GET.get("q", "").strip()

    products = Product.objects.filter(is_active=True)

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(category__name__icontains=q)
        )

    products = products.order_by("name")[:24]

    return render(request, "home.html", {
        "products": products,
        "q": q,
    })



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
from django.shortcuts import render, get_object_or_404
from .models import Order

@login_required
def order_history(request):
    """Show all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/history.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    """Show a single order with its items."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    items_qs = order.items.select_related("product")
    items = []
    for it in items_qs:
        items.append({
            "product": it.product,
            "quantity": it.quantity,
            "price_each": it.price_each,
            "line_total": it.price_each * it.quantity,
        })

    return render(request, "orders/detail.html", {"order": order, "items": items})

from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def reorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    cart = _get_cart(request.session)
    added = 0
    skipped = 0

    for oi in order.items.select_related("product"):
        p = oi.product

        if not p.is_active:
            skipped += 1
            continue

        pid = str(p.id)
        cart[pid] = cart.get(pid, 0) + int(oi.quantity)
        added += 1

    request.session.modified = True
    return HttpResponseRedirect(reverse("cart"))


@login_required
def saved_list(request):
    saved = SavedItem.objects.filter(user=request.user).select_related("product").order_by("-created_at")
    return render(request, "saved/list.html", {"saved": saved})

@login_required
def saved_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    SavedItem.objects.get_or_create(user=request.user, product=product)
    return redirect("saved_list")

@login_required
def saved_remove(request, product_id):
    SavedItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect("saved_list")


@staff_member_required
def courier_dashboard(request):
    available_orders = Order.objects.filter(status="PLACED", courier__isnull=True).order_by("created_at")
    my_orders = Order.objects.filter(courier=request.user).exclude(status="DELIVERED").order_by("created_at")

    return render(request, "courier/dashboard.html", {
        "available_orders": available_orders,
        "my_orders": my_orders,
    })


@staff_member_required
@require_POST
def courier_claim(request, order_id):
    order = get_object_or_404(Order, id=order_id, status="PLACED", courier__isnull=True)
    order.courier = request.user
    order.status = "ASSIGNED"
    order.save()
    return redirect("courier_dashboard")


@staff_member_required
@require_POST
def courier_mark_out(request, order_id):
    order = get_object_or_404(Order, id=order_id, courier=request.user)
    if order.status == "ASSIGNED":
        order.status = "OUT"
        order.save()
    return redirect("courier_dashboard")


@staff_member_required
@require_POST
def courier_mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id, courier=request.user)
    if order.status in ("ASSIGNED", "OUT"):
        order.status = "DELIVERED"
        order.save()
    return redirect("courier_dashboard")



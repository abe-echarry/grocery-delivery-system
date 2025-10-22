from django.urls import path
from . import views
urlpatterns = [ path('', views.home, name='home') ]

#Cart
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_view, name="cart"),                 
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
]

#protect checkout
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    
# checkout
    path("checkout/", login_required(views.checkout), name="checkout"),
    path("order/success/<int:order_id>/", login_required(views.order_success), name="order_success"),
    
#order history
    path("orders/", login_required(views.order_history), name="order_history"),
    path("orders/<int:order_id>/", login_required(views.order_detail), name="order_detail"),
 
  
]


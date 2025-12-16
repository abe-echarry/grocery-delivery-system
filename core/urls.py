from django.urls import path
from . import views

urlpatterns = [
    # home
    path("", views.home, name="home"),

    # cart
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),

    # checkout
    path("checkout/", views.checkout, name="checkout"),
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),

    # order history + detail
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

    #reorder
    path("orders/<int:order_id>/reorder/", views.reorder, name="reorder"),

        
    # saved items
    path("saved/", views.saved_list, name="saved_list"),
    path("saved/add/<int:product_id>/", views.saved_add, name="saved_add"),
    path("saved/remove/<int:product_id>/", views.saved_remove, name="saved_remove"),


    # courier
    path("courier/", views.courier_dashboard, name="courier_dashboard"),
    path("courier/claim/<int:order_id>/", views.courier_claim, name="courier_claim"),
    path("courier/out/<int:order_id>/", views.courier_mark_out, name="courier_mark_out"),
    path("courier/delivered/<int:order_id>/", views.courier_mark_delivered, name="courier_mark_delivered"),


]



from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove-from-cart/<str:key>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/", views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("payment/", views.payment, name="payment"),

    # 🔐 AUTH
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]

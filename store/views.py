from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Order, OrderItem

# HOME
def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


# PRODUCT DETAIL
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store/product_detail.html", {"product": product})


# ADD TO CART
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get("size")
    quantity = int(request.POST.get("quantity", 1))

    cart = request.session.get("cart", {})
    key = f"{product_id}_{size}"

    if key in cart:
        cart[key]["quantity"] += quantity
    else:
        cart[key] = {
            "product_id": product_id,
            "size": size,
            "quantity": quantity,
        }

    request.session["cart"] = cart
    return redirect("cart")


# VIEW CART
def cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    for key, item in cart.items():
        product = get_object_or_404(Product, id=item["product_id"])
        quantity = item["quantity"]

        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            "key": key,
            "product": product,
            "size": item["size"],
            "quantity": quantity,
            "item_total": item_total,
        })

    gst = total_price * 0.18
    grand_total = total_price + gst

    return render(request, "store/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "gst": gst,
        "grand_total": grand_total,
    })


# REMOVE FROM CART
def remove_from_cart(request, key):
    cart = request.session.get("cart", {})
    if key in cart:
        del cart[key]
    request.session["cart"] = cart
    return redirect("cart")


# 🔐 CHECKOUT (LOGIN REQUIRED)
@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    total_price = 0
    cart_items = []

    for item in cart.values():
        product = Product.objects.get(id=item["product_id"])
        quantity = item["quantity"]
        size = item["size"]

        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "size": size,
            "price": product.price,
        })

    gst = total_price * 0.18
    grand_total = total_price + gst

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            gst=gst,
            grand_total=grand_total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                size=item["size"],
                quantity=item["quantity"],
                price=item["price"],
            )

        request.session["cart"] = {}

        return redirect("order_success")

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "gst": gst,
        "grand_total": grand_total,
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "store/my_orders.html", {"orders": orders})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != "CANCELLED":
        order.status = "CANCELLED"
        order.save()

    return redirect("my_orders")

# SUCCESS
def order_success(request):
    return render(request, "store/order_success.html")


# 🔐 LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "store/login.html", {"error": "Invalid credentials"})

    return render(request, "store/login.html")


# 🔐 SIGNUP
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "store/signup.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")

    return render(request, "store/signup.html")


# 🔐 LOGOUT
def logout_view(request):
    logout(request)
    return redirect("home")

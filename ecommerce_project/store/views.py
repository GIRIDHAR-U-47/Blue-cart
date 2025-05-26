from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Product added to cart")
    return redirect('product_list')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty")
        return redirect('product_list')
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        Order.objects.create(user=request.user, product=product, quantity=quantity)
    request.session['cart'] = {}
    messages.success(request, "Order placed successfully!")
    return redirect('product_list')

from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

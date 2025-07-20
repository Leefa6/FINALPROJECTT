# shop/views.py
# This file contains the logic for handling requests and returning responses for the shop app.
# Each function is a 'view' that connects to a URL route and renders a template or returns data.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import NewUserForm, ProductForm
from .models import Product, Category, Review
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponseForbidden

# Utility function to check if user is staff or superuser
# Use this with @user_passes_test(is_admin_or_staff) for admin-only views

def is_admin_or_staff(user):
    """
    Returns True if the user is a staff member or superuser (admin privileges).
    Use this to restrict product management views.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Context processor: Adds cart summary data to every template automatically.
def cart_context(request):
    """
    This function runs for every request and adds cart info to the template context.
    It lets you show cart items/count/total in the navbar on every page.
    """
    cart = request.session.get('cart', {})  # Get the cart dictionary from the session
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    cart_count = 0
    cart_total = Decimal('0.00')
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        cart_total += subtotal
        cart_count += quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return {
        'cart_items_nav': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }

# Home page view: shows the landing page.
def home(request):
    """
    Renders the home page template with latest products.
    """
    from .models import Product
    latest_products = Product.objects.order_by('-id')[:3]
    return render(request, "shop/home.html", {"latest_products": latest_products})

# About page view: shows info about the store.
def about(request):
    """
    Route: '/about/'
    Renders the about page template.
    """
    return render(request, "shop/about.html")

# Shop view: shows all products, with optional category filtering.
def shop_view(request):
    """
    Route: '/shop/'
    Shows a list of all products. If a category is selected (via ?category=slug), filters products by that category.
    Passes products, categories, and selected_category to the template for display and filtering UI.
    """
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.all()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, "shop/shop.html", context)

# Product detail view: shows info for a single product, reviews, and recommendations.
def product_detail(request, slug):
    """
    Route: '/shop/<slug:slug>/'
    Shows details for a single product, its reviews, and up to 4 recommended products from the same category.
    Passes the product and recommendations to the template.
    """
    product = get_object_or_404(Product, slug=slug)
    recommendations = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, "shop/detail.html", {"product": product, "recommendations": recommendations})

# Add to cart view: handles adding a product to the session-based cart.
def add_to_cart(request, slug):
    """
    Route: '/add-to-cart/<slug:slug>/'
    On POST, adds the product to the cart stored in the session. Increments quantity if already present.
    Redirects to the cart page and shows a message.
    If the request is AJAX (fetch or XMLHttpRequest), return JSON with cart count and success message instead of redirecting.
    """
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})
    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1
    request.session['cart'] = cart  # Save the updated cart back to the session
    # Calculate new cart count
    cart_count = sum(cart.values())
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': f"Added {product.name} to cart."
        })
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('cart')

# Remove from cart view: removes a product from the session cart.
def remove_from_cart(request, slug):
    """
    Route: '/remove-from-cart/<slug:slug>/'
    Removes the product from the session cart and redirects to the cart page.
    """
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})
    if str(product.id) in cart:
        del cart[str(product.id)]
        request.session['cart'] = cart
        messages.info(request, f"Removed {product.name} from cart.")
    return redirect('cart')

# Cart view: shows the contents of the user's cart (from session).
@login_required
def cart_view(request):
    """
    Route: '/cart/'
    Retrieves the cart from the session, fetches product objects and quantities, calculates subtotals and total.
    Passes cart_items and total to the template for display.
    """
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = Decimal('0.00')
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, "shop/cart.html", context)

# Checkout view: placeholder for future checkout logic.
@login_required
def checkout_view(request):
    """
    Route: '/checkout/'
    Shows the checkout page (not implemented in detail here).
    """
    return render(request, "shop/checkout.html")

# User registration view: handles new user sign up.
def register_request(request):
    """
    Route: '/register/'
    Handles user registration using NewUserForm. On success, logs in the user and redirects to dashboard.
    Passes the form to the template for display.
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request, "shop/register.html", {"form": form})

# User login view: handles authentication.
def login_request(request):
    """
    Route: '/login/'
    Handles user login using AuthenticationForm. On success, logs in the user and redirects to dashboard.
    Passes the form to the template for display.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "shop/login.html", {"form": form})

# User logout view: logs out the user and redirects to home.
def logout_request(request):
    """
    Route: '/logout/'
    Logs out the user and redirects to the home page with a message.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

# User dashboard view: shows user info (requires login).
@login_required
def dashboard(request):
    """
    Route: '/dashboard/'
    Shows the user dashboard page (requires authentication).
    """
    return render(request, "shop/dashboard.html")

# AJAX review submission view: handles review form via JavaScript fetch.
@require_POST
@login_required
def submit_review(request, slug):
    """
    Route: '/shop/<slug:slug>/review/'
    Accepts POST requests from the review form (AJAX/fetch).
    Validates and saves the review, then returns JSON with the new review data.
    Used by the JavaScript in detail.html to update the reviews list without reloading.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=403)
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST
        rating = data.get('rating')
        comment = data.get('comment')
        if not rating or not comment:
            return JsonResponse({'error': 'Rating and comment are required.'}, status=400)
        product = get_object_or_404(Product, slug=slug)
        review = Review.objects.create(
            user=request.user,
            product=product,
            rating=int(rating),
            comment=comment
        )
        return JsonResponse({
            'reviewer': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    return JsonResponse({'error': 'Invalid request.'}, status=400)

# Add product view: allows only staff to add new products.
@login_required
@user_passes_test(is_admin_or_staff)
def add_product(request):
    """
    Allows only staff to add new products. Only accessible to logged-in staff.
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to add products.")
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('shop')
    else:
        form = ProductForm()
    return render(request, "shop/add_product.html", {"form": form})

@login_required
def edit_product(request, slug):
    """
    Allow the creator of a product to edit its details.
    Only the user who created the product can edit it.
    """
    product = get_object_or_404(Product, slug=slug)
    if product.created_by != request.user:
        return redirect('product_detail', slug=product.slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

def contact(request):
    """
    Renders the contact page with a contact form and store info.
    """
    return render(request, 'shop/contact.html')
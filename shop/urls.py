# shop/urls.py
# This file maps URL patterns to view functions in the shop app.
# Import Django's path function to define URL patterns
from django.urls import path
# Import views from the current package
from . import views

# List of URL patterns for the shop app
urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # About page
    path('about/', views.about, name='about'),
    # Shop page (all products, with optional category filtering)
    path('shop/', views.shop_view, name='shop'),
    # Add product (staff only)
    path('shop/add/', views.add_product, name='add_product'),
    # Product detail page (uses product slug for clean URLs)
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
    # AJAX review submission for a product
    path('shop/<slug:slug>/review/', views.submit_review, name='submit_review'),
    # User registration
    path('register/', views.register_request, name='register'),
    # User login
    path('login/', views.login_request, name='login'),
    # User logout
    path('logout/', views.logout_request, name='logout'),
    # User dashboard (requires login)
    path('dashboard/', views.dashboard, name='dashboard'),
    # Shopping cart page (requires login)
    path('cart/', views.cart_view, name='cart'),
    # Add a product to the cart (by slug)
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    # Remove a product from the cart (by slug)
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    # Checkout page (requires login)
    path('checkout/', views.checkout_view, name='checkout'),
    path('shop/<slug:slug>/edit/', views.edit_product, name='edit_product'),
]
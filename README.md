# Django Clothing Store

A simple, student-friendly Django web app for an online clothing store. Features product browsing, cart, reviews, authentication, and admin product management.

## Features
- Product catalog with categories
- User registration, login, logout
- Shopping cart (session-based)
- Product reviews (AJAX)
- Admin/staff product management
- Responsive Bootstrap 5 forms (crispy_forms)
- Image uploads (pillow)

## Requirements
- Python 3.10+
- Django 5.2.4
- django-crispy-forms 2.4
- crispy-bootstrap5 2025.6
- pillow 11.3.0
- sqlparse 0.5.3
- asgiref 3.9.1

Install all requirements with:
```bash
pip install -r requirements.txt
```

## Setup & Usage
1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd clothing_store2
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure
- `shop/` - Main app (models, views, forms, URLs)
- `templates/` - HTML templates (layout, shop, detail, cart, etc.)
- `static/` - Static files (CSS, JS, images)
- `products/` - Uploaded product images
- `config/` - Project settings and URLs

## Notes
- Uses session for cart (no database cart model)
- Uses crispy_forms for Bootstrap 5 form styling
- Uses pillow for image uploads
- All logic is beginner-friendly and commented for learning

---

Feel free to fork, modify, and use for your coursework or demos! 
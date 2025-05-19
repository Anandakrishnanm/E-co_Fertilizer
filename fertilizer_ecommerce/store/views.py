from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import Cart
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



# Login View
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if user.is_admin:
                return redirect('admin_home')
            elif user.is_buyer:
                return redirect('buyer_home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')



def home(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'home.html', {'products': products})


@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})

# @login_required
# def buyer_dashboard(request):
#     if not request.user.is_buyer:
#         return redirect('login')

#     query = request.GET.get('q', '')  # Get search input
#     category_filter = request.GET.get('category', '')  # Get filter selection

#     products = Product.objects.all()

#     # Apply search filter
#     if query:
#         products = products.filter(name__icontains=query)

#     # Apply category filter
#     if category_filter:
#         products = products.filter(category=category_filter)

#     return render(request, 'buyer_dashboard.html', {'products': products, 'query': query, 'category_filter': category_filter})


@login_required
def buyer_dashboard(request):
    if not request.user.is_buyer:
        return redirect('login')

    # Get search and filter inputs
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()

    # Get all products
    products = Product.objects.all()

    # Handle comma-separated search queries
    if search_query:
        search_terms = [term.strip().rstrip('.') for term in search_query.split(",") if term.strip()]
        query = Q()
        for term in search_terms:
            query |= (Q(name__icontains=term))

        products = products.filter(query)

    # Apply category filter if provided
    if category_filter:
        products = products.filter(category=category_filter)

    return render(request, 'buyer_dashboard.html', {'products': products})





@login_required
def buyer_home(request):
    if not request.user.is_buyer:
        return redirect('login')
    return render(request, 'buyer_home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered!'})

        # Create new buyer user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_buyer = True  # Mark as buyer
        user.save()

        # Auto-login the user after registration
        login(request, user)
        return redirect('buyer_dashboard')

    return render(request, 'register.html')


#######################################################
# Admin: View all products
@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})

# Admin: Add Product
@login_required
def add_product(request):
    if not request.user.is_admin:
        return redirect('login')

    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        image = request.FILES.get('image')  # Handle image upload

        Product.objects.create(name=name, description=description, price=price, category=category, image=image)
        return redirect('admin_dashboard')

    return render(request, 'add_product.html')

# Admin: Edit Product
@login_required
def edit_product(request, product_id):
    if not request.user.is_admin:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.category = request.POST['category']
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_product.html', {'product': product})

# Admin: Delete Product
@login_required
def delete_product(request, product_id):
    if not request.user.is_admin:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_dashboard')


##############################


@login_required
def admin_home(request):
    return render(request, 'admin_home.html')

# @login_required
# def order_management(request):
#     orders = Order.objects.all()
#     return render(request, 'order_management.html', {'orders': orders})

@login_required
def order_management(request):
    if not request.user.is_admin:
        return redirect('login')

    orders = Order.objects.all()

    # Add total_price dynamically
    for order in orders:
        order.total_price = order.quantity * order.product.price

    return render(request, 'order_management.html', {'orders': orders})



@login_required
def user_management(request):
    users = User.objects.filter(is_admin=False)  # Get only buyers
    return render(request, 'user_management.html', {'users': users})

@login_required
def admin_profile(request):
    admin = request.user

    if request.method == "POST":
        admin.username = request.POST['username']
        admin.email = request.POST['email']
        admin.save()
        return redirect('admin_home')

    return render(request, 'admin_profile.html', {'admin': admin})

@login_required
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        order.status = request.POST['status']
        order.save()
    return redirect('order_management')

@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('user_management')


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def admin_change_password(request):
    if not request.user.is_admin:  # Ensure only admin can access this page
        messages.error(request, "Unauthorized Access!")
        return redirect('home')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the admin logged in
            messages.success(request, "Password updated successfully!")
            return redirect('admin_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)  # Show empty form initially

    return render(request, 'admin_change_password.html', {'form': form})



####################################################################################################
##################################################################

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})




@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum(item.total_price() for item in cart_items)  # Call method

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart! 🛒")
    return redirect('view_cart')



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get("quantity", 1))

    # Try to get an existing cart item
    cart_item = Cart.objects.filter(user=request.user, product=product).first()

    if cart_item:
        # If it exists, update the quantity
        cart_item.quantity += quantity
    else:
        # If it doesn't exist, create a new cart item
        cart_item = Cart(user=request.user, product=product, quantity=quantity)

    cart_item.save()

    # Update cart count in session
    request.session["cart_count"] = Cart.objects.filter(user=request.user).count()

    messages.success(request, f"{product.name} added to cart! 🛒")
    return redirect("view_cart")



@login_required
def checkout(request):
    if not request.user.is_buyer:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Your cart is empty! Add products before checking out.")
        return redirect('buyer_dashboard')

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Create orders from cart items
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                status="Pending",  # Default status
                full_name=full_name,  # Save buyer details
                address=address,
                phone=phone
            )

        # Clear the cart after order is placed
        cart_items.delete()

        messages.success(request, "✅ Order placed successfully!")
        return redirect('order_history')  # Redirects to order history page

    # Calculate total price for each cart item
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


from django.shortcuts import render
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    # Add total_price calculation for each order
    for order in orders:
        order.total_price = order.quantity * order.product.price  

    return render(request, 'order_history.html', {'orders': orders})



@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != "Delivered":  # Ensure delivered orders can't be canceled
        order.status = "Canceled"
        order.save()

    return redirect('order_history')  # Redirect back to Order History page




@login_required
def buyer_profile(request):
    return render(request, 'buyer_profile.html', {'user': request.user})

# @login_required
# def edit_profile(request):
#     if request.method == "POST":
#         form = ProfileUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('buyer_profile')
#     else:
#         form = ProfileUpdateForm(instance=request.user)
    
#     return render(request, 'edit_profile.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("buyer_home")

    return render(request, "edit_profile.html", {"user": request.user})





@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, "Password changed successfully!")
            return redirect('buyer_profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})


from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class BuyerPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('buyer_home')  # Redirect to Buyer Home after password change


@login_required
def buyer_profile(request):
    return render(request, 'buyer_profile.html')
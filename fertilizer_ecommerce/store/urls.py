from django.urls import path
from django.urls import path, include
from .views import user_login, user_logout, admin_dashboard, buyer_dashboard, register, edit_product, delete_product, add_product,admin_home ,admin_profile
from .views import order_management, user_management,update_order_status, delete_user, home, buyer_profile, admin_change_password
from .views import buyer_home, product_detail, view_cart, remove_from_cart, add_to_cart, checkout, order_history, cancel_order, edit_profile, BuyerPasswordChangeView

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('buyer-dashboard/', buyer_dashboard, name='buyer_dashboard'),
    path('register/', register, name='register'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('admin-home/', admin_home, name='admin_home'),
    path('order-management/', order_management, name='order_management'),
    path('user-management/', user_management, name='user_management'),
    path('admin-profile/', admin_profile, name='admin_profile'),
    path('buyer-home/', buyer_home, name='buyer_home'),
    path('admin-change-password/', admin_change_password, name='admin_change_password'),
]

urlpatterns += [
    path('', home, name='home'),  # Home page
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-history/', order_history, name='order_history'),
    path('cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('change-password/', BuyerPasswordChangeView.as_view(), name='change_password'),
    path('buyer/profile/', buyer_profile, name='buyer_profile'),  # Ensure this exists
]


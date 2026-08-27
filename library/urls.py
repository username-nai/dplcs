from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('request-borrow/', views.request_borrow, name='request_borrow'),
    
    # Admin URLs
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-user-borrowed/<int:user_id>/', views.admin_user_borrowed, name='admin_user_borrowed'),
    path('admin-requests/', views.admin_requests, name='admin_requests'),
    path('admin-handle-request/<int:request_id>/<str:action>/', views.admin_handle_request, name='admin_handle_request'),
    
    # Return Requests
    path('request-return/<int:borrowed_book_id>/', views.request_return, name='request_return'),
    path('admin-return-requests/', views.admin_return_requests, name='admin_return_requests'),
    path('admin-handle-return/<int:request_id>/<str:action>/', views.admin_handle_return, name='admin_handle_return'),
]

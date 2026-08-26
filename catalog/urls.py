from django.urls import path
from . import views

urlpatterns = [
    path('find/', views.find_book, name='find_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-find/', views.admin_find_book, name='admin_find_book'),
    path('admin-add/', views.admin_add_book, name='admin_add_book'),
    path('admin-change-quantity/<int:book_id>/<str:action>/', views.admin_change_quantity, name='admin_change_quantity'),
    path('admin-delete/<int:book_id>/', views.admin_delete_book, name='admin_delete_book'),
]

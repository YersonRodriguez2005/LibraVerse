#Importaciones
from django.urls import path
from . import views
from .views import add_book, admin_books
from django.conf import settings
from django.conf.urls.static import static

#Definición de Urls a nivel de aplicación
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('protected/', views.protected_view, name='protected'),
    path('search/', views.search_books, name='search'),
    path('catalog/', views.catalog, name='catalog'),  
    path('books/', views.view_books, name='view_books'),
    path('add-book/', views.add_book, name='add_book'),    
    path('admin_books/', admin_books, name='admin_books'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
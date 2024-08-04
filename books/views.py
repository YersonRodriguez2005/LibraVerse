from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import CustomUserCreationForm, BookForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# Mostrar interfaz renderizado de home
def home(request):
    latest_books = Book.objects.filter(approved=True).order_by('-id')[:5]
    return render(request, 'home.html', {'latest_books': latest_books})


# Mostrar interfaz renderizado de register
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Mostrar interfaz renderizado de login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Metodo de logout
def user_logout(request):
    logout(request)
    return redirect('home')

# Proteger su cuenta
@login_required
def protected_view(request):
    return render(request, 'protected.html')

# Metodo de busqueda de libros por filtro
def search_books(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )
    return render(request, 'books/search_results.html', {'results': results, 'query': query})

# Mostrar interfaz renderizado de catalog
def catalog(request):
    return render(request, 'catalog.html')

# Metodo de interfaz administrador
@login_required
def admin_dashboard(request):
    books = Book.objects.all().order_by('-created_at')[:10]  # Obtener los últimos 10 libros agregados
    return render(request, 'admin_dashboard.html', {'books': books})

# Metodo de añadir libro
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro ha sido agregado exitosamente.')
            return redirect('admin_books')  # Redirige a la vista de administración
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro ha sido editado exitosamente.')
            return redirect('admin_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'El libro ha sido eliminado.')
        return redirect('admin_books')
    return render(request, 'books/delete_book.html', {'book': book})

@login_required
def admin_books(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'books/admin_books.html', {'books': books})

@login_required
def approve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.approved = True
    book.save()
    messages.success(request, 'El libro ha sido aprobado.')
    return redirect('admin_books')

#Metodo para vista de lirbos: def view_books(request):
def view_books(request):
    books = Book.objects.all()
    return render(request, 'view_books.html', {'books': books})
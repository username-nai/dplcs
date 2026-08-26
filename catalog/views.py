from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Book, Author
from .forms import BookForm

@login_required
def find_book(request):
    query = request.GET.get('q', '')
    books = []
    if query:
        books = Book.objects.filter(
            Q(name__icontains=query) | Q(authors__name__icontains=query)
        ).distinct()
        if not books:
            messages.info(request, "No book found. Please provide correct information.")
    return render(request, 'catalog/find_book.html', {'books': books, 'query': query})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'catalog/book_detail.html', {'book': book})

@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role:
        return redirect('user_dashboard')
    return render(request, 'catalog/admin_dashboard.html')

@login_required
def admin_find_book(request):
    if not request.user.is_admin_role:
        return redirect('home')
    query = request.GET.get('q', '')
    books = []
    if query:
        books = Book.objects.filter(
            Q(name__icontains=query) | Q(authors__name__icontains=query)
        ).distinct()
        if not books:
            messages.info(request, "No book found. Please provide correct information.")
    return render(request, 'catalog/admin_find_book.html', {'books': books, 'query': query})

@login_required
def admin_add_book(request):
    if not request.user.is_admin_role:
        return redirect('home')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.available_quantity = book.total_quantity
            book.save()
            
            author_names = [name.strip() for name in form.cleaned_data['author_name'].split(',') if name.strip()]
            for author_name in author_names:
                author, created = Author.objects.get_or_create(name__iexact=author_name, defaults={'name': author_name})
                book.authors.add(author)
                
            messages.success(request, "Book added successfully!")
            return redirect('admin_add_book')
    else:
        form = BookForm()
        
    return render(request, 'catalog/admin_add_book.html', {'form': form})

@login_required
def admin_change_quantity(request, book_id, action):
    if not request.user.is_admin_role:
        return redirect('home')
        
    book = get_object_or_404(Book, id=book_id)
    borrowed_count = book.total_quantity - book.available_quantity
    
    if action == 'increase':
        book.total_quantity += 1
        book.available_quantity += 1
        book.save()
        messages.success(request, f"Quantity increased. Total is now {book.total_quantity}.")
    elif action == 'decrease':
        if book.total_quantity > borrowed_count:
            book.total_quantity -= 1
            book.available_quantity -= 1
            book.save()
            messages.success(request, f"Quantity decreased. Total is now {book.total_quantity}.")
        else:
            messages.error(request, "Quantity cannot be less than currently borrowed copies.")
            
    return redirect('admin_find_book') # Assuming we redirect back to search or we can redirect to book detail

@login_required
def admin_delete_book(request, book_id):
    if not request.user.is_admin_role:
        return redirect('home')
        
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        borrowed_count = book.total_quantity - book.available_quantity
        if borrowed_count > 0:
            messages.error(request, "This book cannot be deleted because copies are currently borrowed.")
        else:
            book.delete()
            messages.success(request, "Book deleted successfully.")
        return redirect('admin_find_book')
        
    return render(request, 'catalog/admin_delete_book.html', {'book': book})

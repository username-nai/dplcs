from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem, BorrowRequest, BorrowedBook
from catalog.models import Book
from accounts.models import User

@login_required
def user_dashboard(request):
    if request.user.is_admin_role:
        return redirect('admin_dashboard')
        
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    borrowed_books = request.user.borrowed_books.all().order_by('-borrow_date')
    
    return render(request, 'library/user_dashboard.html', {
        'cart_items': cart_items,
        'borrowed_books': borrowed_books
    })

@login_required
def add_to_cart(request, book_id):
    if request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if book.available_quantity <= 0:
            messages.error(request, "This book is currently out of stock.")
            return redirect('book_detail', book_id=book.id)
            
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
        
        if not item_created:
            if cart_item.quantity + 1 > book.available_quantity:
                messages.error(request, "Requested quantity exceeds available copies.")
            else:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, f"Increased quantity of {book.name} in your cart.")
        else:
            messages.success(request, f"{book.name} added to your cart.")
            
    return redirect('user_dashboard')

@login_required
def remove_from_cart(request, item_id):
    if request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('user_dashboard')

@login_required
def update_cart(request, item_id, action):
    if request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if action == 'increase':
            if cart_item.quantity + 1 > cart_item.book.available_quantity:
                messages.error(request, "Requested quantity exceeds available copies.")
            else:
                cart_item.quantity += 1
                cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('user_dashboard')

@login_required
def request_borrow(request):
    if request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('user_dashboard')
            
        with transaction.atomic():
            for item in cart_items:
                # Check for existing pending request for same book
                existing_request = BorrowRequest.objects.filter(
                    user=request.user, book=item.book, status='Pending'
                ).exists()
                
                if existing_request:
                    messages.warning(request, f"You already have a pending request for {item.book.name}.")
                    continue
                
                # Create request
                BorrowRequest.objects.create(
                    user=request.user,
                    book=item.book,
                    quantity=item.quantity
                )
                
            # Clear the cart items that were requested
            cart_items.delete()
            messages.success(request, "Borrow request submitted successfully.")
            
    return redirect('user_dashboard')

@login_required
def admin_users(request):
    if not request.user.is_admin_role:
        return redirect('home')
        
    users = User.objects.filter(is_admin_role=False)
    return render(request, 'library/admin_users.html', {'users': users})

@login_required
def admin_user_borrowed(request, user_id):
    if not request.user.is_admin_role:
        return redirect('home')
        
    user = get_object_or_404(User, id=user_id, is_admin_role=False)
    borrowed_books = user.borrowed_books.all().order_by('-borrow_date')
    return render(request, 'library/admin_user_borrowed.html', {
        'member': user,
        'borrowed_books': borrowed_books
    })

@login_required
def admin_requests(request):
    if not request.user.is_admin_role:
        return redirect('home')
        
    requests = BorrowRequest.objects.all().order_by('-request_date')
    return render(request, 'library/admin_requests.html', {'requests': requests})

@login_required
def admin_handle_request(request, request_id, action):
    if not request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        borrow_req = get_object_or_404(BorrowRequest, id=request_id)
        
        if borrow_req.status != 'Pending':
            messages.error(request, f"Request is already {borrow_req.status}.")
            return redirect('admin_requests')
            
        if action == 'confirm':
            with transaction.atomic():
                # Re-fetch book to avoid race conditions
                book = Book.objects.select_for_update().get(id=borrow_req.book.id)
                if book.available_quantity >= borrow_req.quantity:
                    book.available_quantity -= borrow_req.quantity
                    book.save()
                    
                    borrow_req.status = 'Approved'
                    borrow_req.save()
                    
                    BorrowedBook.objects.create(
                        user=borrow_req.user,
                        book=book,
                        quantity=borrow_req.quantity
                    )
                    messages.success(request, f"Request approved. Inventory updated.")
                else:
                    messages.error(request, f"Not enough available copies for {book.name}.")
                    
        elif action == 'decline':
            borrow_req.status = 'Declined'
            borrow_req.save()
            messages.success(request, "Request declined.")
            
    return redirect('admin_requests')

@login_required
def request_return(request, borrowed_book_id):
    if request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        from .models import ReturnRequest
        borrowed = get_object_or_404(BorrowedBook, id=borrowed_book_id, user=request.user)
        
        if ReturnRequest.objects.filter(borrowed_book=borrowed, status='Pending').exists():
            messages.warning(request, "You already have a pending return request for this book.")
        else:
            ReturnRequest.objects.create(user=request.user, borrowed_book=borrowed)
            messages.success(request, "Return request submitted successfully.")
            
    return redirect('user_dashboard')

@login_required
def admin_return_requests(request):
    if not request.user.is_admin_role:
        return redirect('home')
        
    from .models import ReturnRequest
    requests = ReturnRequest.objects.all().order_by('-request_date')
    return render(request, 'library/admin_return_requests.html', {'requests': requests})

@login_required
def admin_handle_return(request, request_id, action):
    if not request.user.is_admin_role:
        return redirect('home')
        
    if request.method == 'POST':
        from .models import ReturnRequest
        return_req = get_object_or_404(ReturnRequest, id=request_id)
        
        if return_req.status != 'Pending':
            messages.error(request, f"Request is already {return_req.status}.")
            return redirect('admin_return_requests')
            
        if action == 'confirm':
            with transaction.atomic():
                book = Book.objects.select_for_update().get(id=return_req.borrowed_book.book.id)
                qty = return_req.borrowed_book.quantity
                
                book.available_quantity += qty
                book.save()
                
                return_req.status = 'Approved'
                return_req.save()
                
                return_req.borrowed_book.delete()
                
                messages.success(request, "Return approved. Inventory updated.")
        elif action == 'decline':
            return_req.status = 'Declined'
            return_req.save()
            messages.success(request, "Return request declined.")
            
    return redirect('admin_return_requests')

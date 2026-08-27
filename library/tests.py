from django.test import TestCase
from accounts.models import User
from catalog.models import Book, Author
from library.models import Cart, CartItem, BorrowRequest

class SystemTests(TestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_user(username='admin_test', phone='00', is_admin_role=True, password='p')
        self.user = User.objects.create_user(username='user_test', phone='11', password='p')
        
        # Create book
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            name='Test Book', total_quantity=5, available_quantity=5,
            room_no='1', shelf_no='1', row='1', column='1'
        )
        self.book.authors.add(self.author)

    def test_user_creation_member_id(self):
        self.assertTrue(self.user.member_id.startswith('LIB'))
        self.assertNotEqual(self.admin.member_id, self.user.member_id)
        
    def test_cart_auto_creation(self):
        self.assertTrue(Cart.objects.filter(user=self.user).exists())
        self.assertFalse(Cart.objects.filter(user=self.admin).exists())

    def test_add_to_cart_and_quantity_limit(self):
        self.client.login(username=self.user.member_id, password='p')
        
        # Add 1 to cart
        self.client.post(f'/library/add-to-cart/{self.book.id}/')
        cart = Cart.objects.get(user=self.user)
        item = CartItem.objects.get(cart=cart, book=self.book)
        self.assertEqual(item.quantity, 1)
        
        # Try to increase past availability (5)
        for _ in range(10):
            self.client.post(f'/library/update-cart/{item.id}/increase/')
            
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_borrow_request_workflow(self):
        self.client.login(username=self.user.member_id, password='p')
        self.client.post(f'/library/add-to-cart/{self.book.id}/')
        
        # Request borrow
        self.client.post('/library/request-borrow/')
        
        # Cart should be empty
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 0)
        
        # Request should be pending
        req = BorrowRequest.objects.get(user=self.user, book=self.book)
        self.assertEqual(req.status, 'Pending')
        
        # Admin approves
        self.client.logout()
        self.client.login(username=self.admin.member_id, password='p')
        self.client.post(f'/library/admin-handle-request/{req.id}/confirm/')
        
        # Check inventory and request status
        req.refresh_from_db()
        self.book.refresh_from_db()
        
        self.assertEqual(req.status, 'Approved')
        self.assertEqual(self.book.available_quantity, 4)

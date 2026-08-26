from django.core.management.base import BaseCommand
from accounts.models import User
from catalog.models import Author, Book

class Command(BaseCommand):
    help = 'Load sample data for testing the Public Library Digital Catalog System MVP'

    def handle(self, *args, **kwargs):
        # Create Admin
        if not User.objects.filter(phone='0000000000').exists():
            admin = User.objects.create_user(
                username='admin',
                password='adminpassword',
                phone='0000000000',
                email='admin@library.local',
                first_name='System Admin',
                is_admin_role=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: Member ID: {admin.member_id}, Password: adminpassword'))

        # Create Members
        if not User.objects.filter(phone='1111111111').exists():
            user1 = User.objects.create_user(
                username='user1',
                password='user1password',
                phone='1111111111',
                email='alice@library.local',
                first_name='Alice Smith'
            )
            self.stdout.write(self.style.SUCCESS(f'Created member: Member ID: {user1.member_id}, Password: user1password'))

        if not User.objects.filter(phone='2222222222').exists():
            user2 = User.objects.create_user(
                username='user2',
                password='user2password',
                phone='2222222222',
                email='bob@library.local',
                first_name='Bob Johnson'
            )
            self.stdout.write(self.style.SUCCESS(f'Created member: Member ID: {user2.member_id}, Password: user2password'))

        # Create Authors
        author1, _ = Author.objects.get_or_create(name='Abraham Silberschatz')
        author2, _ = Author.objects.get_or_create(name='Henry F. Korth')
        author3, _ = Author.objects.get_or_create(name='Thomas H. Cormen')

        # Create Books
        book1, created = Book.objects.get_or_create(
            name='Database System Concepts',
            defaults={
                'total_quantity': 4,
                'available_quantity': 4,
                'room_no': '203',
                'shelf_no': '07',
                'row': '3',
                'column': '5'
            }
        )
        if created:
            book1.authors.add(author1, author2)

        book2, created = Book.objects.get_or_create(
            name='Introduction to Algorithms',
            defaults={
                'total_quantity': 10,
                'available_quantity': 10,
                'room_no': '204',
                'shelf_no': '01',
                'row': '1',
                'column': '1'
            }
        )
        if created:
            book2.authors.add(author3)

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data.'))

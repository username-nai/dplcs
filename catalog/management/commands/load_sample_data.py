from django.core.management.base import BaseCommand
from accounts.models import User
from catalog.models import Author, Book

class Command(BaseCommand):
    help = 'Load sample data for testing the Public Library Digital Catalog System MVP'

    def handle(self, *args, **kwargs):
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
        author4, _ = Author.objects.get_or_create(name='Robert C. Martin')
        author5, _ = Author.objects.get_or_create(name='Andrew S. Tanenbaum')
        author6, _ = Author.objects.get_or_create(name='Erich Gamma')
        author7, _ = Author.objects.get_or_create(name='Richard Helm')
        author8, _ = Author.objects.get_or_create(name='Ralph Johnson')
        author9, _ = Author.objects.get_or_create(name='John Vlissides')
        author10, _ = Author.objects.get_or_create(name='Martin Fowler')
        author11, _ = Author.objects.get_or_create(name='Stuart Russell')
        author12, _ = Author.objects.get_or_create(name='Peter Norvig')
        author13, _ = Author.objects.get_or_create(name='Donald Knuth')
        author14, _ = Author.objects.get_or_create(name='Harold Abelson')
        author15, _ = Author.objects.get_or_create(name='Gerald Jay Sussman')
        author16, _ = Author.objects.get_or_create(name='Steve McConnell')
        author17, _ = Author.objects.get_or_create(name='Eric Freeman')
        author18, _ = Author.objects.get_or_create(name='Elisabeth Robson')
        author19, _ = Author.objects.get_or_create(name='Brian W. Kernighan')
        author20, _ = Author.objects.get_or_create(name='Dennis M. Ritchie')

        # Books list configuration
        books_data = [
            {
                'name': 'Database System Concepts',
                'defaults': {'total_quantity': 4, 'available_quantity': 4, 'room_no': '203', 'shelf_no': '07', 'row': '3', 'column': '5'},
                'authors': [author1, author2]
            },
            {
                'name': 'Introduction to Algorithms',
                'defaults': {'total_quantity': 10, 'available_quantity': 10, 'room_no': '204', 'shelf_no': '01', 'row': '1', 'column': '1'},
                'authors': [author3]
            },
            {
                'name': 'Clean Code',
                'defaults': {'total_quantity': 5, 'available_quantity': 5, 'room_no': '201', 'shelf_no': '03', 'row': '2', 'column': '4'},
                'authors': [author4]
            },
            {
                'name': 'Modern Operating Systems',
                'defaults': {'total_quantity': 6, 'available_quantity': 6, 'room_no': '203', 'shelf_no': '05', 'row': '4', 'column': '2'},
                'authors': [author5]
            },
            {
                'name': 'Design Patterns: Elements of Reusable Object-Oriented Software',
                'defaults': {'total_quantity': 3, 'available_quantity': 3, 'room_no': '202', 'shelf_no': '09', 'row': '1', 'column': '3'},
                'authors': [author6, author7, author8, author9]
            },
            {
                'name': 'Refactoring: Improving the Design of Existing Code',
                'defaults': {'total_quantity': 4, 'available_quantity': 4, 'room_no': '201', 'shelf_no': '04', 'row': '3', 'column': '1'},
                'authors': [author10]
            },
            {
                'name': 'Artificial Intelligence: A Modern Approach',
                'defaults': {'total_quantity': 8, 'available_quantity': 8, 'room_no': '205', 'shelf_no': '02', 'row': '5', 'column': '2'},
                'authors': [author11, author12]
            },
            {
                'name': 'The Art of Computer Programming, Volume 1',
                'defaults': {'total_quantity': 2, 'available_quantity': 2, 'room_no': '204', 'shelf_no': '08', 'row': '2', 'column': '4'},
                'authors': [author13]
            },
            {
                'name': 'Structure and Interpretation of Computer Programs',
                'defaults': {'total_quantity': 5, 'available_quantity': 5, 'room_no': '204', 'shelf_no': '03', 'row': '4', 'column': '1'},
                'authors': [author14, author15]
            },
            {
                'name': 'Code Complete',
                'defaults': {'total_quantity': 7, 'available_quantity': 7, 'room_no': '201', 'shelf_no': '06', 'row': '1', 'column': '5'},
                'authors': [author16]
            },
            {
                'name': 'Head First Design Patterns',
                'defaults': {'total_quantity': 6, 'available_quantity': 6, 'room_no': '202', 'shelf_no': '10', 'row': '2', 'column': '2'},
                'authors': [author17, author18]
            },
            {
                'name': 'The C Programming Language',
                'defaults': {'total_quantity': 9, 'available_quantity': 9, 'room_no': '203', 'shelf_no': '01', 'row': '3', 'column': '3'},
                'authors': [author19, author20]
            }
        ]

        for b_data in books_data:
            book, created = Book.objects.get_or_create(
                name=b_data['name'],
                defaults=b_data['defaults']
            )
            if created:
                book.authors.add(*b_data['authors'])

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data.'))
from django.core.management.base import BaseCommand
from ecommerceapp.models import Address, Contact, Product, Employee, Network
from django.contrib.auth.models import User
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Очистка старых данных
        models = [Address, Contact, Product, Employee, Network, User]
        for model in models:
            model.objects.all().delete()

        self.stdout.write('Creating new data...')
        
        # Создание тестового пользователя
        user = User.objects.create_user(
            username='testuser',
            password='testpass',
            is_active=True
        )
        
        # Создание адресов и контактов
        contacts = []
        for _ in range(15):
            address = Address.objects.create(
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.building_number()
            )
            contact = Contact.objects.create(
                email=fake.email(),
                address=address
            )
            contacts.append(contact)
        
        # Создание продуктов
        products = []
        tech_words = ['Smart', 'Pro', 'Max', 'Ultra', 'Mini', 'Air', 'Quantum']
        for _ in range(20):
            product = Product.objects.create(
                name=f"{fake.word().capitalize()} {random.choice(tech_words)} {fake.word().capitalize()}",
                model=f"MOD-{fake.bothify(text='??###')}",
                # release_date=fake.date_this_decade()
                release_date=fake.date_between(start_date='-5y', end_date='today')
            )
            products.append(product)
        
        # Создание сетей и сотрудников
        networks = []
        levels = [0, 1, 2, 3, 4] * 5  # Repeat levels for variety

        for i in range(25):
            network = Network.objects.create(
                name=fake.company(),
                level=levels[i],
                debt=random.uniform(0, 10000),
                # contact=Contact.objects.order_by('?').first(),
                contact=random.choice(contacts),
                supplier=None  # Will set later
            )
            network.products.set(random.sample(products, random.randint(1, 5)))
            networks.append(network)
            
            for _ in range(random.randint(2, 5)):
                Employee.objects.create(
                    name=fake.name(),
                    network=network # This will set employee_id in Network
                )
        
        # Установка поставщиков
        # Заводы (level=0) → Дистрибьюторы (level=1) → Дилеры (level=2) и т.д.
        for i, network in enumerate(networks):
            # Только для НЕ-заводов (level > 0)
            if network.level > 0:

                # Ищем всех ПОДХОДЯЩИХ поставщиков:
                # - уровень поставщика ДОЛЖЕН БЫТЬ МЕНЬШЕ уровня текущей сети
                possible_suppliers = [n for n in networks if n.level < network.level]

                # Если нашли подходящих поставщиков
                if possible_suppliers:
                    # Выбираем СЛУЧАЙНОГО поставщика из возможных
                    network.supplier = random.choice(possible_suppliers)
                    network.save()
        
        self.stdout.write(self.style.SUCCESS(f'Database seeded successfully:'
                                           f'\n- {len(contacts)} Contacts'
                                           f'\n- {len(products)} Products'
                                           f'\n- {len(networks)} Networks'
                                           f'\n- {Employee.objects.count()} Employees'))
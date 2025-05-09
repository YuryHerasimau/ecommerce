from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=50, verbose_name='Страна')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house_number = models.CharField(max_length=5, verbose_name='Номер дома')

    class Meta:
        ordering = ('country',)
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house_number}'


class Contact(models.Model):
    email = models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название продукта')
    model = models.CharField(max_length=50, verbose_name='Модель продукта')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} {self.model} ({self.release_date})'


class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя сторудника')
    # Изменил связь с сотрудниками - теперь сотрудники связаны с Network через ForeignKey
    network = models.ForeignKey('Network', on_delete=models.CASCADE, related_name='employees', 
                              null=True, blank=True, verbose_name='Торговая сеть')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name


class Network(models.Model):
    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Дистрибьютор'),
        (2, 'Дилерский центр'),
        (3, 'Крупная розничная сеть'),
        (4, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=50, unique=True, verbose_name='Название сети')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Контакты')
    # Стало: products (т.к. ManyToManyField) и related_name='networks' (какие сети используют этот продукт)
    products = models.ManyToManyField(Product, related_name='networks', verbose_name='Продукты')
    # Убрал отдельную модель Supplier и перенес уровень иерархии в модель Network
    level = models.IntegerField(choices=LEVEL_CHOICES, help_text='Выберите уровень иерархии', default=0, verbose_name='Уровень иерархии')
    # Сделал связь поставщика через ForeignKey на ту же модель Network (self)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставщик', related_name='children')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Торговая сеть'
        verbose_name_plural = 'Торговые сети'

    def __str__(self):
        return self.name

    def get_products(self):
        return ", ".join([product.name for product in self.products.all()])
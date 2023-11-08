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
        return f'{self.country, self.city, self.street, self.house_number}'


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
        return f'{self.name} {self.model}'


class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя сторудника')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.name}'


class Supplier(models.Model):
    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Дистрибьютор'),
        (2, 'Дилерский центр'),
        (3, 'Крупная розничная сеть'),
        (4, 'Индивидуальный предприниматель'),
    )
    name = models.CharField(max_length=50, verbose_name='Наименование поставщика')
    level = models.IntegerField(choices=LEVEL_CHOICES, help_text='Выберите уровень иерархии', default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Network(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название сети')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Контакты')
    product = models.ManyToManyField(Product, related_name='network_products', verbose_name='Продукты')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сотрудники')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставщик')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Торговая сеть'
        verbose_name_plural = 'Торговые сети'

    def __str__(self):
        return self.name

    def get_products(self):
        return ", ".join([product.name for product in self.product.all()])
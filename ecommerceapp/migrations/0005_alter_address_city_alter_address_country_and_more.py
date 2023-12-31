# Generated by Django 4.2.7 on 2023-11-07 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0004_alter_supplier_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(max_length=50, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_number',
            field=models.CharField(max_length=5, verbose_name='Номер дома'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=50, verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.address', verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Имя сторудника'),
        ),
        migrations.AlterField(
            model_name='network',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.contact', verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='network',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='network',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Задолженность перед поставщиком'),
        ),
        migrations.AlterField(
            model_name='network',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.employee', verbose_name='Сотрудники'),
        ),
        migrations.AlterField(
            model_name='network',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название сети'),
        ),
        migrations.AlterField(
            model_name='network',
            name='product',
            field=models.ManyToManyField(related_name='network_products', to='ecommerceapp.product', verbose_name='Продукты'),
        ),
        migrations.AlterField(
            model_name='network',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerceapp.supplier', verbose_name='Поставщик'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.CharField(max_length=50, verbose_name='Модель продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='release_date',
            field=models.DateField(verbose_name='Дата выхода продукта на рынок'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Наименование поставщика'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-07 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0002_supplier_alter_network_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='level',
            field=models.IntegerField(choices=[('Factory', 'Завод'), ('Distributor', 'Дистрибьютор'), ('Dealership', 'Дилерский центр'), ('Large retail network', 'Крупная розничная сеть'), ('Individual entrepreneur', 'Индивидуальный предприниматель')], help_text='Выберите уровень иерархии'),
        ),
    ]

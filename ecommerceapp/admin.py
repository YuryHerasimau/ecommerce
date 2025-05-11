from django.contrib import admin
from .models import Address, Contact, Product, Employee, Network
from .tasks import async_clear_debt


@admin.action(description="Очистить задолженность перед поставщиком у выбранных объектов")
def clear_debt(modeladmin, request, queryset):
    if queryset.count() > 20:
        # Асинхронная обработка для большого количества объектов
        network_ids = list(queryset.values_list('id', flat=True))
        async_clear_debt.delay(network_ids)
        modeladmin.message_user(request, "Запущена фоновая очистка задолженности для выбранных сетей")
    else:
        # Синхронная обработка для малого количества
        queryset.update(debt=0)
        modeladmin.message_user(request, f"Задолженность очищена для {queryset.count()} сетей")


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'get_products', 'level', 'supplier', 'debt', 'created_at')
    list_display_links = ('name', 'supplier', 'debt')
    search_fields = ('contact__address__city',)
    list_filter = ('contact__address__city', 'level')
    actions = [clear_debt]
    inlines = [EmployeeInline]

    def get_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    
    get_products.short_description = 'Продукты'


admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Network, NetworkAdmin)
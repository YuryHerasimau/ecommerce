from django.contrib import admin
from .models import Address, Contact, Product, Employee, Supplier, Network


@admin.action(description="Очистить задолженность перед поставщиком у выбранных объектов")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'get_products', 'employee', 'supplier', 'debt', 'created_at')
    list_display_links = ('name', 'supplier', 'debt')
    search_fields = ('contact__address__city',)
    list_filter = ('contact__address__city',)
    actions = [clear_debt]


admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Network, NetworkAdmin)
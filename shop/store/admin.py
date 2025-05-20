from django.contrib import admin
from .models import Category, Product, ProductImage, ContactsMessage, Order, OrderItem, Attribute, AttributeValue, ProductAttribute


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'category']
    search_fields = ['name', 'description']


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['value']


# store/admin.py
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute', 'value', 'quantity', 'is_available']
    list_filter = ['attribute', 'value']
    search_fields = ['product__name']
    raw_id_fields = ['product']

    def is_available(self, obj):
        return obj.quantity > 0

    is_available.boolean = True
    is_available.short_description = 'Доступен'


@admin.register(ContactsMessage)
class ContactsMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_processed',)
    date_hierarchy = 'created_at'


class OrderItemInline(admin.TabularInline):  # или admin.StackedInline
    model = OrderItem
    extra = 0  # чтобы не показывать пустые формы для новых items


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'city', 'paid', 'created']
    list_filter = ['paid', 'created', 'city']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]  # показываем OrderItems внутри Order


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']
    list_filter = ['order', 'product']


admin.site.register(ProductImage)

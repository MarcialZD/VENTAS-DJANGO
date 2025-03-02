from django.contrib import admin

from .models import *
from django.shortcuts import render,redirect

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Tag)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

    fieldsets = (
        ('Product Information', {
            'fields': ('price', 'description', 'name' , 'category', 'is_active', 'image','tag')
        }),
    )
    ordering = ('-create_at',)
    filter_horizontal = ('tag',)

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        # generamos mensaje
        self.message_user(request, f'Productos desactivados {queryset.count()}')
    make_inactive.short_description = 'Marcar como inactivo'

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        # generamos mensaje
        self.message_user(request, f'Productos activados {queryset.count()}')
        
    make_active.short_description = 'Marcar como activo'

    def set_price(self,request,queryset):
        if 'apply' in request.POST:
            price = request.POST.get('price')
            queryset.update(price=price)
            self.message_user(request,f'Precio actualizado a {price}')
            return redirect(request.get_full_path())
        return render(request,'admin/set_price.html',context={'products':queryset})

    actions = [make_inactive, make_active,set_price]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','total_price','total_items')
    inlines = [CartItemInline]
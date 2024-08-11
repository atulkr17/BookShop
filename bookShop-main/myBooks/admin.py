from django.contrib import admin
from .models import Category,Product,Order
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('c_name',)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def img_prd(self,obj):
        return format_html('<img src = "{}" width= "50" height="50"/>'.format(obj.image.url))
    list_display=('name','description','price','img_prd','author','prev_price','category')    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user', 'address', 'product', 'quantity', 'payment_status')  
    
# Register your models here.

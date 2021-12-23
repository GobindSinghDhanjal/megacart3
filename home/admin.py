from django.contrib import admin
from home.models import Category, Customer, DealsOfTheDay, Product, Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['id','name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['id','name']

#class AdminDeals(admin.ModelAdmin):
 #   list_display = ['Product.id','product.name','product.price','product.category']


# Register your models here.

admin.site.register(Customer)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(DealsOfTheDay)
admin.site.register(Order) 

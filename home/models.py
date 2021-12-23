from django.db import models
from django.db.models.deletion import CASCADE
import datetime

# Create your models here.

#REGISTER/CUSTOMER FORM 

class Customer(models.Model):
    firstName=models.CharField(max_length=20)
    lastName=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=200)
    phone=models.CharField(max_length=10, blank=True)
    address=models.CharField(max_length=1000, blank=True)

#PRODUCT DATABASE

class Category(models.Model):
    name=models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category(categoryId):
        return Category.objects.get(id=categoryId)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=20)
    title=models.CharField(max_length=100,default='')
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=CASCADE,default=1)
    description1=models.CharField(max_length=200,default='')
    description2=models.CharField(max_length=200,blank=True)
    description3=models.CharField(max_length=300,blank=True)
    description4=models.CharField(max_length=300,blank=True)
    description5=models.CharField(max_length=300,blank=True)
    offer1=models.CharField(max_length=300,default='Bank Offer 10% off on any Debit/Credit Cards, up to ₹1500. On orders of ₹5000 and above',blank=True)
    offer2=models.CharField(max_length=300,default='Get a Google Home Mini at just ₹1,499 on purchase of select laptops, TVs, ACs and mobile phones',blank=True)
    image1=models.ImageField(upload_to='uploads/products/')
    image2=models.ImageField(upload_to='uploads/products/',null=True,blank=True)
    image3=models.ImageField(upload_to='uploads/products/',null=True,blank=True)
    image4=models.ImageField(upload_to='uploads/products/',null=True,blank=True)

    @staticmethod
    def get_all_products():
     return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
     return Product.objects.filter(category=category_id)

    @staticmethod
    def get_product_by_id(ids):
     return Product.objects.filter(id=ids)

    @staticmethod
    def get_cart_product_by_id(ids):
        return Product.objects.filter(id__in=ids)

    def __str__(self):
        return self.name

class DealsOfTheDay(models.Model):
    product=models.ForeignKey(Product,on_delete=CASCADE,default=1)

    @staticmethod
    def get_all_deals():
     return DealsOfTheDay.objects.all()

    @staticmethod
    def get_product_by_id(ids):
     return Product.objects.filter(id=ids)


class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    totalPrice=models.IntegerField()
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=13,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')
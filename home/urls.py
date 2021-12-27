from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('homepage',views.homepage,name='homepage'),
    path('product_details',views.product_details,name='product_details'),
    path('cart',views.cart,name='cart'),
    path('account',views.account,name='account'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('addToCart',views.addToCart,name='addToCart'),
    path('logout',views.logout,name='logout'),
    path('all_products',views.all_products,name='all_products'),
    path('about_us',views.about_us,name='about_us'),
    path('check_out',views.check_out,name='check_out'),
    path('orders',views.orderHistory,name='orders'),
    path('phone_save',views.phone_save,name='phone_save'),
    path('address_save',views.address_save,name='address_save'),
    path('payment',views.payment,name='payment'),
    path('search',views.search,name='search'),
    path('orderPlaced',views.orderPlaced,name='orderPlaced')


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

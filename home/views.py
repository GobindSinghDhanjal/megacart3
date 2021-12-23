from django.http import request
from home.models import Category, Customer, DealsOfTheDay, Order, Product, Customer
from django.shortcuts import redirect, render,HttpResponse
from django.utils.decorators import method_decorator

from middleware.auth import auth_middleware

def index(request):
   product=Product.get_all_products() 
   categories=Category.get_all_categories()
   dealsoftheday=DealsOfTheDay.get_all_deals()
   data={}
   data['products'] =product
   data['categories'] =categories
   data['deals']=dealsoftheday
   return render(request,'homepage.html',data)

@staticmethod
def get_product_by_id(ids):
    return Product.objects.filter(id__in=ids)

def homepage(request):
    product=Product.get_all_products() 
    categories=Category.get_all_categories()
    dealsoftheday=DealsOfTheDay.get_all_deals()
    data={}
    data['products'] =product
    data['categories'] =categories
    data['deals']=dealsoftheday
    print("homepage : "+str(request.session.get('email'))) 
    # clear the session   
    #request.session.clear()
    return render(request,'homepage.html',data)

def product_details(request):
    if(request.method=="POST"):
        product=request.POST.get('product')

        cart=request.session.get('cart')

        if cart:
            quantity=cart.get(product)
            if quantity:
                cart[product] = quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1

        request.session['cart']=cart
        print("cart is ",request.session['cart'])

        return redirect('cart')

    else:
        cart=request.session.get('cart')

        if not cart:
            request.session['cart']={}

        productId= request.GET.get('productId')
        products=Product.get_all_products() 
        categories=Category.get_all_categories()
        product=Product.get_product_by_id(productId)
        data={}
        data['product'] =product
        data['products'] =products
        data['categories'] =categories
        print("product : "+str(product))
        cart=request.session.get('cart')
        if not cart:
            request.session['cart'] ={}
            
        return render(request,'product_details.html',data)   


def register(request):
    if (request.method == "POST"):
        firstName=request.POST.get("firstName")
        lastName=request.POST.get("lastName")
        email=request.POST.get("email")
        password=request.POST.get("password")

        Reg=Customer(firstName=firstName,
                     lastName=lastName,
                     email=email,
                     password=password)

        if Customer.objects.filter(email=email):
            msg="Email already exists"
            return render(request,'account.html',{'msg':msg})
        else:
            Reg.save()
            data=Customer.objects.get(email=email,password=password)
            request.session['customer']=data.id
            request.session['name'] = firstName+' '+lastName
            request.session['email']=email
            request.session['phone']=data.phone
            print("CUSTOMER :", request.session['customer'])
            return redirect('homepage')
    else:
        return HttpResponse("try again")

def login(request):
    if(request.method =="POST"):
        email=request.POST['loginEmail']
        password=request.POST['loginPassword']
        #data=Customer.objects.filter(email=email).filter(password=password).all()

        try:
            data=Customer.objects.get(email=email,password=password)
        except:
            data=None

        msg="Try again..."
        if(data):

            request.session['customer']=data.id
            request.session['name'] = data.firstName+' '+data.lastName
            request.session['email']=email
            request.session['phone']=data.phone
            request.session['address']=data.address

            return redirect('homepage')
        else:
            return render(request,'account.html',{'msg':msg})

def logout(request):
    request.session.clear()
    return redirect('account')


def phone_save(request):
    if (request.method == "POST"):
        id=request.session.get('customer')
        phone=request.POST.get("phone")

        data=Customer.objects.get(id=id)
        data.phone=phone
        data.save()
        request.session['phone']=data.phone
        return render(request,'account.html')
    else:
        return HttpResponse("try again")

def address_save(request):
    if (request.method == "POST"):
        id=request.session.get('customer')
        address=request.POST.get("address")

        data=Customer.objects.get(id=id)
        data.address=address
        data.save()
        request.session['address']=data.address
        return render(request,'account.html')
    else:
        return HttpResponse("try again")


def about_us(request):
    return render(request,'about_us.html')

def payment(request):
    return render(request,'payment.html')

def account(request):
    return render(request,'account.html')

def cart(request):
    print(request.session.get('cart'))
    if not request.session.get('cart'):
        return render(request,'cart.html',{'products':None})
    ids = list(request.session.get('cart').keys())
    products=Product.get_cart_product_by_id(ids)
    print(products)
    return render(request,'cart.html',{'products':products})

def addToCart(request):
    if(request.method=="POST"):
        productId=request.POST.get('productId')
        

        product=request.POST.get('productId')
        cart=request.session.get('cart')

        if cart:
            quantity=cart.get(product)
            if quantity:
                cart[product]=1+quantity
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        
        request.session['cart']=cart

        
        print(request.session['cart'])

        return redirect('product_details')
    else:
        return render(request,'product_details.html')

def all_products(request):
    categories=Category.get_all_categories()
    categoryId= request.GET.get('category')

    products=Product.get_all_products_by_category_id(categoryId)

    data={}
    data['products'] =products
    data['categories'] =categories
    data['category']=Category.get_category(categoryId)
    return render(request,'all_products.html',data)

def productAndCategory():
    product=Product.get_all_products() 
    categories=Category.get_all_categories()
    data={}
    data['products'] =product
    data['categories'] =categories
    return data

@auth_middleware
def check_out(request):
    print("request " ,request.POST)
    customer=request.session.get('customer')
    cart=request.session.get('cart')
    products=Product.get_cart_product_by_id(list(cart.keys()))
    print("Customer ",customer,cart,products)

    for product in products:
        order=Order(customer=Customer(id=customer),
                    product=product,
                    price=product.price,
                    quantity=cart.get(str(product.id)),
                    totalPrice=product.price*cart.get(str(product.id)))
        order.save()

    request.session['cart']={}

    return redirect('orders')

@auth_middleware
def orderHistory(request):
    customer=request.session.get('customer')
    orders=Order.get_orders_by_customer(customer)
    print(orders)
    return render(request,'orders.html',{'orders':orders})




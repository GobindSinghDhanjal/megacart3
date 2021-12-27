from django.http import request
from home.models import Category, Customer, DealsOfTheDay, Order, Product, Customer
from django.shortcuts import redirect, render,HttpResponse
from django.utils.decorators import method_decorator

from middleware.auth import auth_middleware

def index(request):
#    product=Product.get_all_products() 
   categories=Category.get_all_categories()
   dealsoftheday=DealsOfTheDay.get_all_deals()
   phone = Product.get_all_products_by_category_id(1)[:7]
   laptop = Product.get_all_products_by_category_id(3)[:7]
   tv=Product.get_all_products_by_category_id(4)[:7]
   product={
       'phone':phone,
       'laptop':laptop,
       'tv':tv}
   data={}
   data['products'] =product
   data['categories'] =categories
   data['deals']=dealsoftheday
   return render(request,'homepage.html',data)

@staticmethod
def get_product_by_id(ids):
    return Product.objects.filter(id__in=ids)

def homepage(request):
    return index(request)

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
        
        categories=Category.get_all_categories()
        product=Product.get_product_by_id(productId)

        productCategory = list(Product.get_cart_product_by_id(product).values_list('category', flat=True))
        try:
            products=Product.get_all_products_by_category_id(int(productCategory[0]))[:7]
            
        except:
            return redirect('homepage')

        productCategory=str(productCategory[0])
        data={}
        data['product'] =product
        data['products'] =products
        data['categories'] =categories
        data['productCategory']=productCategory
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

def search(request):
    if(request.method == "POST"):
        searchProduct=request.POST['searchProduct']
        searchedProducts = Product.objects.filter(title__contains=searchProduct)

        data={}
        data['products'] =searchedProducts

        return render(request,'search.html',data)
    else:
        return render(request,'search.html')

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

    try:
        categoryId= int(request.GET.get('category'))
    except:
        categoryId=0

    data={}

    if(categoryId==0):
        products=Product.get_all_products()
        data['category']="All Products"
    else:
         products=Product.get_all_products_by_category_id(categoryId)
         data['categories'] =categories
         data['category']=Category.get_category(categoryId)
   


    data['products'] =products

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
    if (request.method=="POST"):
        print(request.session['cart'])
        return payment(request)

    else:
        # customer=request.session.get('customer')
        # cart=request.session.get('cart')
        # products=Product.get_cart_product_by_id(list(cart.keys()))
        # print("Customer ",customer,cart,products)

        # for product in products:
        #     order=Order(customer=Customer(id=customer),
        #             product=product,
        #             price=product.price,
        #             quantity=cart.get(str(product.id)),
        #             totalPrice=product.price*cart.get(str(product.id)))
        # order.save()

        # request.session['cart']={}

        # return redirect('orders')
        return redirect('cart')

def payment(request):
    return render(request,'payment.html')

def orderPlaced(request):
    if (request.method=="POST"):
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        print("CArt "+str(cart))
        phone=request.POST['phone']
        address=request.POST['address']

        products=Product.get_cart_product_by_id(list(cart.keys()))
        print("Customer ",customer,cart,products)

        for product in products:
            order=Order(customer=Customer(id=customer),
                    product=product,
                    price=product.price,
                    quantity=cart.get(str(product.id)),
                    totalPrice=product.price*cart.get(str(product.id)),
                    phone=phone,
                    address=address)
            order.save()
        


        request.session['cart']={}

        return redirect('orders')
    else:
        return HttpResponse("wrong")

@auth_middleware
def orderHistory(request):
    customer=request.session.get('customer')
    orders=Order.get_orders_by_customer(customer)
    print(orders)
    return render(request,'orders.html',{'orders':orders})




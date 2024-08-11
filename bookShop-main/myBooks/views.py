import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .forms import MyRegFrm,LoginFrm
from .models import Category,Product,CartItem,Orderr
from django.db.models import F
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.core.mail import send_mail
from django.db.models import Q


def home(request):
    c=Category.objects.all()
    p=Product.objects.order_by('?')[:12]
    bu=Product.objects.all().filter(category__c_name='business')
    te=Product.objects.all().filter(category__c_name='technology')
    ro=Product.objects.all().filter(category__c_name='romantic')
    ad=Product.objects.all().filter(category__c_name='adventure')
    fi=Product.objects.all().filter(category__c_name='fictional')
    offer=Product.objects.filter(price__lt=F('prev_price'))
    ba=Product.objects.order_by('?')[:3]
    f=Product.objects.order_by('?')[:4]
    if request.user.is_authenticated:
        x=1
    else:
        x=0    
    
    
    return render(request,'myBooks/index.html',{'c':c,'p':p,'bu':bu,'te':te,'ro':ro,'ad':ad,'fi':fi,'ba':ba,'offer':offer,'f':f,'x':x})
    
def signup(request):
    form1=LoginFrm()
    if request.POST:
        
        if 'register' in request.POST:
            form=MyRegFrm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request,'your registraion is succesfull')
                except Exception as e:
                    messages.error(request,e)
        elif 'login' in request.POST: 
            form=MyRegFrm()           
            form1=LoginFrm(request=request,data=request.POST)
            if form1.is_valid():
                uname=form1.cleaned_data['username']
                upass=form1.cleaned_data['password']    
                user=authenticate(username=uname,password=upass)    
                if user is not None:
                    login(request,user)
                    return redirect('/')       


    else:
        
        form=MyRegFrm()
    return render(request,'myBooks/signup.html',{'form': form, 'form1': form1})  
def signout(request):
    logout(request)
    return redirect('/')
def add_to_cart(request,p_id):
    if request.user.is_authenticated:
        product=Product.objects.get(p_id=p_id)
        cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
        cart_item.quantity+=1
        cart_item.save()
        return redirect('/allcart')
    else:
        return redirect('/signup')
def rm_to_cart(request,p_id):
    if request.user.is_authenticated:
        product=Product.objects.get(p_id=p_id)
        cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
        cart_item.quantity-=1
        cart_item.save()
        if cart_item.quantity<1:
            cart_item.delete()
        return redirect('/allcart')
    else:
        return redirect('/signup')
def viewCart(request):
    if request.user.is_authenticated:
        p=Product.objects.all()
        cart_items=CartItem.objects.filter(user=request.user) 
        total_price=sum(item.product.price*item.quantity for item in cart_items)
        total_price=int(total_price)
        if request.user.is_authenticated:
            x=1
        else:
            x=0 
        return render(request, 'myBooks/viewCart.html',{'cart_items':cart_items,'total_price':total_price,'x':x,'p':p})
    else:
        return redirect('/signup')
    
def removeCart(request,id):
    if request.user.is_authenticated:
        cart_items=CartItem.objects.get(id=id,user=request.user) 
        cart_items.delete()
        return redirect('/allcart')
        if request.user.is_authenticated:
            x=1
        else:
            x=0 
        return render(request, 'myBooks/viewCart.html',{'cart_items':cart_items,'total_price':total_price,'x':x})
    else:
        return redirect('/signup')   
def add_to_cart_m(request, p_id):
    # Logic to add item to cart
    # ...

    # Pass a message to the template context
    message = 'Item added to cart successfully.'

    return redirect('/')  
def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # Amount in paise
        address=request.POST['address']
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)
        
        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZOR_KEY_ID,
            "name": "My Project",
            "description": "Payment for Your Product",
            "image": "https://yourwebsite.com/logo.png",  # Replace with your logo URL
        }
        cart_items=CartItem.objects.filter(user=request.user)
        # payment_id=response_data.id
        for cart in cart_items:
            Orderr.objects.get_or_create(user=request.user, product= cart.product, quantity=cart.quantity, payment_status='success', address=address)
        
        CartItem.objects.filter(user=request.user).delete()

        return JsonResponse(response_data)
    return redirect('/allcart') 
def payment_success(request):
    return render(request, "myBooks/viewOrders.html")

def payment_failed(request):
    return render(request, "myBooks/payment_failed.html") 
@login_required
def viewOrders(request):
    cart_items = Orderr.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_price = int(total_price)
    first_name = request.user.first_name
    last_name=request.user.last_name
    mobile = request.user.mobile  # Assuming 'mobile' is the name of the field
    x = 1  # Assuming you always set x to 1 if the user is authenticated
    return render(request, 'myBooks/viewOrders.html', {'cart_items': cart_items, 'total_price': total_price, 'x': x,'last_name':last_name, 'first_name': first_name, 'mobile': mobile})
def allprod(request):
    if request.user.is_authenticated:
        x=1
    else:
        x=0
    c=Category.objects.all()
    p=Product.objects.order_by('?')[:12]
    bu=Product.objects.all().filter(category__c_name='business')
    te=Product.objects.all().filter(category__c_name='technology')
    ro=Product.objects.all().filter(category__c_name='romantic')
    ad=Product.objects.all().filter(category__c_name='adventure')
    fi=Product.objects.all().filter(category__c_name='fictional')

    return render (request,'myBooks/allprod.html',{'x':x,'c':c,'p':p,'bu':bu,'te':te,'ro':ro,'ad':ad,'fi':fi})    
def profile(request):
    x=0
    if request.user.is_authenticated:
        x=1
        first_name=request.user.first_name
        last_name=request.user.last_name
        mobile=request.user.mobile
        username=request.user.username
        email=request.user.email
    return render(request,'mybooks/profile.html',{'x':x,'first_name':first_name,'last_name':last_name,'mobile':mobile,'username':username,'email':email})


def contact_us(request):
    if request.user.is_authenticated:
        x=1
    else:
        x=0
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['email']
            recipients = [settings.CONTACT_EMAIL]  # Change to your email
            send_mail(subject, message, sender_email, recipients)
            return HttpResponse('/thanks/')  # Redirect after successful form submission
    else:
        form = ContactForm()
    return render(request, 'myBooks/contact_us.html', {'form': form,'x':x})
def search_results(request):
    if request.user.is_authenticated:
        x=1
    else:
        x=0
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(Q(name__icontains=query))
    else:
        results =Product.objects.all()
    return render(request, 'myBooks/search_results.html', {'results': results, 'x':x,'query': query})

def viewitem(request,p_id):
    items=Product.objects.get(p_id=p_id)
    bu=Product.objects.exclude(p_id=p_id).order_by('?')[:5]
   
    if request.user.is_authenticated:
        x=1
    else:
        x=0
    return render(request,'myBooks/item.html',{'bu':bu,'items':items,'x':x})

# Create your views here.

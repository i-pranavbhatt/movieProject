from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .models import User,movie,m_rating, Client, Customer, cart, OrderItem
from .form import CustomerRegistrationForm, CustomerProfileForm
from django.http import JsonResponse
# Create your views here.

from django.http import HttpResponse

class movieview(View):
    def get(self, request):
        Bol = movie.objects.filter(movie_ge='B')
        Hol = movie.objects.filter(movie_ge='H')
        return render(request, 'myapp1/index.html', {'Bol': Bol, 'Hol': Hol}) #white match to bol variable

def address(request):
    add = Customer.objects.filter(cus_user=request.user)
    return render(request,'myapp1/add.html', {'add':add, 'active':'btn-primary'})

#def home(request):
    #return render(request, 'myapp1/index.html')

#def movie_detail(request):
    #return render(request, 'myapp1/movie_detail.html')

class movie_detail_view(View):
    def get(self, request, pk):
        mo = movie.objects.get(pk=pk)
        return render(request, 'myapp1/movie_detail.html', {'mo':mo})



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'myapp1/signup.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Successfully Register!')
            form.save()
        return render(request, 'myapp1/signup.html', {'form': form})


def movie_list(request, data=None):
    if data == None:
        m_page = movie.objects.filter()
    return render(request, 'myapp1/movie_list.html', {'m_page':m_page})

def movie_filter(request, data=None):
    if data == 'B':
        mbb_page = movie.objects.filter(movie_ge='B')
    else:
        mbb_page = movie.objects.filter(movie_ge='H')
    return render(request, 'myapp1/bollywood.html', {'mbb_page':mbb_page})

def mycart(request):
    u = request.user
    movie_id = request.GET.get('prod_id')
    print(movie_id)
    m = movie.objects.get(id=movie_id)
    cart(user=u, o_movie=m).save()
    return redirect('cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        c = cart.objects.filter(user=user)
        print(c)
        amount = 0.0
        membership_amount = 00.00
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == user]  #get all cart object
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamout = (p.o_quantity * p.o_movie.m_price)
                amount += tempamout
                total_amount = amount + membership_amount
            return render(request,'myapp1/cart.html', {'carts':c, 'total_amount':total_amount, 'amount':amount})
        else:
            return render(request, 'myapp1/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(o_movie=prod_id) & Q(user=request.user))
        c.o_quantity+=1
        c.save()
        amount = 0.0
        membership_amount = 00.00
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]  # get all cart object
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamout = (p.o_quantity * p.o_movie.m_price)
                amount += tempamout


            data ={'quantity':c.o_quantity,
                   'amount': amount,
                   'total_amount': amount + membership_amount}
            return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(o_movie=prod_id) & Q(user=request.user))
        c.o_quantity-=1
        c.save()
        amount = 0.0
        membership_amount = 00.00
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]  # get all cart object
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamout = (p.o_quantity * p.o_movie.m_price)
                amount += tempamout


            data ={'quantity':c.o_quantity,
                   'amount': amount,
                   'total_amount': amount + membership_amount}
            return JsonResponse(data)

def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(o_movie=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        membership_amount = 00.00
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]  # get all cart object
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamout = (p.o_quantity * p.o_movie.m_price)
                amount += tempamout


            data ={'amount': amount,
                   'total_amount': amount + membership_amount}
            return JsonResponse(data)



def top(request, data=None):
    if data == None:
        topm = movie.objects.filter(mo_rating__gt=8)[:5]
    return render(request, 'myapp1/top.html', {'topm':topm})

def checkout(request):
    user = request.user
    add = Customer.objects.filter(cus_user=user)
    cart_iteams = cart.objects.filter(user=user)
    amount = 0.0
    membership_amount = 00.00
    total_amount = 0.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]  # get all cart object
    print(cart_product)
    if cart_product:
        for p in cart_product:
            tempamout = (p.o_quantity * p.o_movie.m_price)
            amount += tempamout
            total_amount = amount + membership_amount
    return render(request,'myapp1/checkout.html',{'add':add, 'total_amount':total_amount, 'cart_iteams':cart_iteams})

def base(request):
    return render(request, 'myapp1/base.html')

def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    Cart = cart.objects.filter(user=user)
    for c in Cart:
        OrderItem(user=user, client=customer, movie=c.o_movie, quantity=c.o_quantity).save()
        c.delete()
    return redirect("orders")

def orders(request):
    op = OrderItem.objects.filter(user=request.user)
    return render(request,'myapp1/orders.html',{'order_paced':op})

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm= AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, 'Login Successfully..!!')
                    return HttpResponseRedirect('/profile')
        else:
            fm = AuthenticationForm()
        return render(request, 'myapp1/login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/profile')


#profile
# def user_profile(request):
#     if request.user.is_authenticated:
#         return render(request, 'myapp1/profile.html', {'name': request.user})
#     else:
#         return HttpResponseRedirect('myapp1/login.html')

class user_profile(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,'myapp1/profile.html',{'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['c_name']
            locality = form.cleaned_data['c_locality']
            city = form.cleaned_data['c_city']
            zipcode = form.cleaned_data['c_zipcode']
            reg = Customer(cus_user=usr, c_name=name, c_locality=locality, c_city=city, c_zipcode=zipcode)
            reg.save()
            messages.success(request, 'congrats..!! Profile Update Successfully')
        return render(request,'myapp1/profile.html',{'form':form, 'active':'btn-primary'})


#logout
def user_logout(request):
    logout(request)
    return redirect('home')



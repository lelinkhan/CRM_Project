from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm,CustomerForm
from .filters import orderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for ' + username)
            return redirect('login')
    content = {'form': form}
    return render(request, 'accounts/register.html', content)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username Or Password is Incorrect!')
            return render(request, 'accounts/login.html')
    content = {}
    return render(request, 'accounts/login.html', content)


def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def UserPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    content = {
        'orders':orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/user.html', content)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSetting(request):
    customers = request.user.customer
    form = CustomerForm(instance=customers)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customers)
        if form.is_valid():
            form.save()

    content = {'form':form}
    return render(request,'accounts/account_setting.html',content)


@login_required(login_url='login')
@admin_only
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    content = {
        'customers': customers,
        'orders': orders,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    content = {'products': products}
    return render(request, 'accounts/products.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    total_orders = orders.count()
    myFilter = orderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    content = {'customers': customers,
               'orders': orders,
               'total_orders': total_orders,
               'myFilter': myFilter
               }
    return render(request, 'accounts/customer.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    # OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    # form_set = OrderFormSet(queryset=Order.objects.none(), instance=customers)
    customers = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customers})
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=customers)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, pk):
    orders = Order.objects.get(id=pk)
    form = OrderForm(instance=orders)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')
    content = {'form': form}
    return render(request, 'accounts/order_form.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def RemoveOrder(request, pk):
    orders = Order.objects.get(id=pk)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')
    content = {'orders': orders}
    return render(request, 'accounts/delete.html', content)

from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.http import HttpResponse
# from extra_views import CreateWithInlinesView, UpdateWithInlinesView,\
#     InlineFormSetFactory
from django.forms import inlineformset_factory
#from django.forms.models import inlineformset_factory
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' +username)
            return redirect('accounts1:login')

    context = {
        'form':form,
    }
    return render(request, 'accounts1/register.html', context)
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username,
                            password = password)
        if user is not None:
            login(request, user)
            return redirect('accounts1:home')
        else:
            messages.info(request, 'username or password is incorrect')
    context = { }
    return render(request, 'accounts1/login.html', context)
def logoutUser(request):
    logout(request)
    return redirect('accounts1:login')
@login_required(login_url = 'accounts1:login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders =orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders':orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers':total_customers,
        'delivered':delivered,
        'pending':pending,
    }

    return render(request, 'accounts1/dashboard.html', context)
@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts1/user.html', context)
@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer  )
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return  redirect('accounts1:account')
    context = { 'form': form }
    return render(request, 'accounts1/account_settings.html', context)

@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts1/products.html', {'products':products})
@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    # a way of querying the customers child object from the model using "order_set"
    orders = customers.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    #this sends a request based on the filter to the queryset,
    # its results are now saved as the new "orders"
    orders = myFilter.qs
    #results come out as a queryset(qs)

    context = {
        'customer': customers,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
    }


    return render(request, 'accounts1/customer.html', context)
@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['admin'])
def createOrder(request, pk):
    #to create multiple forms in one page, use formset
    # inlineform_factory takes in atleast three parameters, parent, child,
    # and child-fields allowed (as list strings in ()) respectively. extra defines number of formsets to display
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product','status'), extra = 5)
    customer = Customer.objects.get(id=pk)
    #then create an instance of the customer to be displayed in the form
    #form = OrderForm(initial = {'customer':customer})
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    #queryset here defines the kind initial data to be displayed in formset
    if request.method == 'POST':
        #print('printing post:', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('../../.')
    context = {
        #'form':form,
         'formset': formset,
    }

    return render(request, 'accounts1/order_form.html', context )
@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('printing post:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accounts1:home')

    context = {
        'form': form,
    }

    return render(request, 'accounts1/order_form.html', context)
@login_required(login_url = 'accounts1:login')
@allowed_user(allowed_rolls= ['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('accounts1:home')
    context = {
        'item': order,
    }

    return render(request, 'accounts1/delete.html', context)
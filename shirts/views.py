from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login as loginUser
from .models import *
from django.db.models import Min
from math import floor
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import request
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from store.settings import API_KEY, AUTH_TOKEN 
from instamojo_wrapper import Instamojo


API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# Create your views here.
def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
    
def home(request):
    products = TheDealSpot.objects.all().order_by("-created_at")
    context = {'prod':products}
    return render(request, 'index.html', context)


def product_detail(request, slug):
    details = TheDealSpot.objects.get(slug=slug)
    size = request.GET.get('size')
    if size is None:
        size = details.sizevariant_set.all().order_by('price').first()
    else:
        size = details.sizevariant_set.get(size=size)
    size_price = size.price
    sell_price = floor(size_price - (size_price * (details.discount)/100)) #This is discount equation
    context = {'details':details, 'price':size_price, 'sell_price':sell_price, 'active_size':size,}
    return render(request, 'prod_details.html', context)    
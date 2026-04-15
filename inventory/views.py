#from django.http import HttpResponse

# Create your views here.

#def home(request):
 #   return HttpResponse("Welcome to the School Inventory System")
#

from django.shortcuts import render
from .models import Item

def home(request):
    return render(request, 'inventory/home.html')


def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/items.html', {'items': items})
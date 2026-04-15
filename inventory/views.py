#from django.http import HttpResponse

# Create your views here.

#def home(request):
 #   return HttpResponse("Welcome to the School Inventory System")
#

from django.shortcuts import render
from .models import Item

from django.shortcuts import redirect
from .models import Request

def home(request):
    return render(request, 'inventory/home.html')


def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/items.html', {'items': items})

def request_item(request, item_id):
    item = Item.objects.get(id=item_id)
    user = request.user
    
    Requesr.objects.create(user=user, item=item)
    return redirect('item_list')
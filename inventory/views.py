#from django.http import HttpResponse

# Create your views here.

#def home(request):
 #   return HttpResponse("Welcome to the School Inventory System")
#

from django.shortcuts import render
from .models import Item
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required   

from django.shortcuts import redirect
from .models import Request

def home(request):
    return render(request, 'inventory/home.html')


def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/items.html', {'items': items})


@login_required
def request_item(request, item_id):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('home')

    item = Item.objects.get(id=item_id)
    Request.objects.create(user=request.user, item=item)
    return redirect('item_list')

@login_required
def manage_requests(request):
    if not request.user.groups.filter(name='Staff').exists():
        return redirect('home')

    requests = Request.objects.all()
    return render(request, 'inventory/manage_requests.html', {'requests': requests})

@login_required
def approve_request(request, request_id):
    if not request.user.groups.filter(name='Staff').exists():
        return redirect('home')

    req = Request.objects.get(id=request_id)
    req.status = 'APPROVED'
    req.save()
    return redirect('manage_requests')

@login_required
def reject_request(request, request_id):
    if not request.user.groups.filter(name='Staff').exists():
        return redirect('home')

    req = Request.objects.get(id=request_id)
    req.status = 'REJECTED'
    req.save()
    return redirect('manage_requests')
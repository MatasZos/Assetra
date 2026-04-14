from django.shortcuts import render

#from django.http import HttpResponse

# Create your views here.

#def home(request):
 #   return HttpResponse("Welcome to the School Inventory System")
#

from django.shortcuts import render

def home(request):
    return render(request, 'inventory/home.html')
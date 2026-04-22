
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 
from .models import Item, Category, Request
from .forms import ItemForm, CategoryForm
 
def is_staff(user):
    return user.groups.filter(name='Staff').exists()
 
def is_student(user):
    return user.groups.filter(name='Student').exists()
 
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
 
@login_required
def home(request):
    if is_staff(request.user):
        return redirect('staff_dashboard')
    if is_manager(request.user):
        return redirect('manager_dashboard')
    return render(request, 'inventory/home.html')
 
 
def item_list(request):
    items = Item.objects.select_related('category').all()
    return render(request, 'inventory/items.html', {'items': items})
 
 
# Student role
 
@login_required
def my_requests(request):
    requests = Request.objects.filter(user=request.user).select_related('item')
    return render(request, 'inventory/my_requests.html', {'requests': requests})
 
 
@login_required
def my_items(request):
    items = Request.objects.filter(user=request.user, status='APPROVED').select_related('item')
    return render(request, 'inventory/my_items.html', {'items': items})
 
 
@login_required
def request_item(request, item_id):
    if not is_student(request.user):
        return redirect('home')
 
    item = get_object_or_404(Item, id=item_id)
 
    if item.quantity <= 0:
        messages.error(request, "This item is out of stock.")
        return redirect('item_list')
 
    Request.objects.create(user=request.user, item=item)
    messages.success(request, f"Request for '{item.name}' submitted successfully.")
    return redirect('item_list')
 
 
@login_required
def return_item(request, request_id):
    req = get_object_or_404(Request, id=request_id)
 
    if req.user != request.user:
        return redirect('home')
 
    if req.status != 'APPROVED':
        messages.warning(request, "Only approved items can be returned.")
        return redirect('my_items')
 
    req.item.quantity += 1
    req.item.save()
    req.status = 'RETURNED'
    req.save()
 
    messages.success(request, "Item returned successfully!")
    return redirect('my_items')
 
 
# Staff role
@login_required
def staff_dashboard(request):
    if not is_staff(request.user):
        return redirect('home')
    return render(request, 'inventory/staff_dashboard.html')
 
 
@login_required
def manage_requests(request):
    if not is_staff(request.user):
        return redirect('home')
 
    pending = Request.objects.filter(status='PENDING').select_related('user', 'item')
    return render(request, 'inventory/manage_requests.html', {'requests': pending})
 
 
@login_required
def approve_request(request, request_id):
    if not is_staff(request.user):
        return redirect('home')
 
    req = get_object_or_404(Request, id=request_id)
 
    if req.status != 'PENDING':
        messages.warning(request, "This request has already been processed.")
        return redirect('manage_requests')
 
    if req.item.quantity <= 0:
        messages.error(request, "Item is out of stock.")
        return redirect('manage_requests')
 
    req.item.quantity -= 1
    req.item.save()
    req.status = 'APPROVED'
    req.save()
 
    messages.success(request, "Request approved successfully!")
    return redirect('manage_requests')
 
 
@login_required
def reject_request(request, request_id):
    if not is_staff(request.user):
        return redirect('home')
 
    req = get_object_or_404(Request, id=request_id)
 
    if req.status != 'PENDING':
        messages.warning(request, "This request has already been processed.")
        return redirect('manage_requests')
 
    req.status = 'REJECTED'
    req.save()
 
    messages.success(request, "Request rejected.")
    return redirect('manage_requests')
 
 
@login_required
def add_stock(request, item_id):
    if not is_staff(request.user):
        return redirect('home')
 
    item = get_object_or_404(Item, id=item_id)
    item.quantity += 1
    item.save()
 
    messages.success(request, f"Stock increased for '{item.name}'.")
    return redirect('item_list')
 
 
# Manager role 

@login_required
def manager_dashboard(request):
    if not is_manager(request.user):
        return redirect('home')
 
    total_items = Item.objects.count()
    total_requests = Request.objects.count()
    pending_count = Request.objects.filter(status='PENDING').count()
    total_categories = Category.objects.count()
 
    context = {
        'total_items': total_items,
        'total_requests': total_requests,
        'pending_count': pending_count,
        'total_categories': total_categories,
    }
    return render(request, 'inventory/manager_dashboard.html', context)
 
 
@login_required
def add_item(request):
    if not is_manager(request.user):
        return redirect('home')
 
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Item '{item.name}' added successfully.")
            return redirect('item_list')
    else:
        form = ItemForm()
 
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Add Item'})
 
 
@login_required
def edit_item(request, item_id):
    if not is_manager(request.user):
        return redirect('home')
 
    item = get_object_or_404(Item, id=item_id)
 
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item '{item.name}' updated successfully.")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
 
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Edit Item'})
 
 
@login_required
def delete_item(request, item_id):
    if not is_manager(request.user):
        return redirect('home')
 
    item = get_object_or_404(Item, id=item_id)
 
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f"Item '{item_name}' deleted.")
        return redirect('item_list')
 
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})
 
 
@login_required
def add_category(request):
    if not is_manager(request.user):
        return redirect('home')
 
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' added successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm()
 
    return render(request, 'inventory/category_form.html', {'form': form, 'action': 'Add Category'})
 
 
@login_required
def edit_category(request, category_id):
    if not is_manager(request.user):
        return redirect('home')
 
    category = get_object_or_404(Category, id=category_id)
 
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
 
    return render(request, 'inventory/category_form.html', {'form': form, 'action': 'Edit Category'})
 
 
@login_required
def category_list(request):
    if not is_manager(request.user):
        return redirect('home')
 
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})
 
 
@login_required
def all_requests(request):
    if not is_manager(request.user):
        return redirect('home')
 
    requests = Request.objects.select_related('user', 'item').order_by('-request_date')
    return render(request, 'inventory/all_requests.html', {'requests': requests})
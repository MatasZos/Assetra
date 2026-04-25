from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Category, Item, Request


def make_user(username, group_name, password='password'):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = User.objects.create_user(username=username, password=password)
    user.groups.add(group)
    return user


#unit test

class ModelUnitTests(TestCase):
    def test_item_quantity_can_be_updated(self):
        cat = Category.objects.create(name='Sports', description='PE gear')
        item = Item.objects.create(name='Football', description='A football', quantity=10, category=cat)
        item.quantity = 7
        item.save()
        item.refresh_from_db()
        self.assertEqual(item.quantity, 7)

    def test_user_assigned_to_correct_group(self):
        user = make_user('testuser', 'Manager')
        self.assertTrue(user.groups.filter(name='Manager').exists())


#integration test and use case test

class UseCaseTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', description='Tech')
        self.item = Item.objects.create(name='Laptop', description='Dell Laptop', quantity=5, category=self.category)
        self.student = make_user('user1', 'Student')
        self.staff = make_user('staff1', 'Staff')
        self.manager = make_user('manager1', 'Manager') 

    def test_item_list_is_visible(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)

    def test_student_can_request_item(self):
        self.client.login(username='user1', password='password')
        self.client.get(reverse('request_item', args=[self.item.id]))
        self.assertEqual(Request.objects.count(), 1)

    def test_staff_can_approve_request(self):
        req = Request.objects.create(user=self.student, item=self.item, status='PENDING')
        self.client.login(username='staff1', password='password')
        self.client.get(reverse('approve_request', args=[req.id]))
        req.refresh_from_db()
        self.assertEqual(req.status, 'APPROVED')

    def test_student_cannot_access_manage_requests(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('manage_requests'))
        self.assertRedirects(response, '/')

    def test_login_required_to_make_request(self):
        response = self.client.get(reverse('request_item', args=[self.item.id]))
        self.assertIn('/login/', response['Location'])
        
    def test_manager_can_create_item_via_form(self):
        self.client.login(username='manager1', password='password')
        self.client.post(reverse('add_item'), {'name': 'Form Test Item','description': 'Created via the add item form','quantity': 5,'category': self.category.id,})
        self.assertTrue(Item.objects.filter(name='Form Test Item').exists())
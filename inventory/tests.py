from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Item, Request
from django.contrib.auth.models import Group


class ModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.user = User.objects.create(username="testuser")
    def test_create_item(self):
        item = Item.objects.create(name="Laptop", description="Dell Laptop",quantity=10,category=self.category)
        self.assertEqual(item.name, "Laptop")
        self.assertEqual(item.quantity, 10)
    def test_create_request(self):
        item = Item.objects.create(name="Mouse",description="Wireless Mouse",quantity=5,category=self.category)
        request = Request.objects.create(user=self.user,item=item)
        self.assertEqual(request.status, "PENDING")


class ViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.user = User.objects.create_user(username="testuser", password="password")
        self.item = Item.objects.create(name="Laptop",description="Dell Laptop",quantity=10,category=self.category)

    def test_item_list_view(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)

    def test_request_item_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('request_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)  


class UseCaseTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.user = User.objects.create_user(username="student", password="password")
        group = Group.objects.create(name="Student")
        self.user.groups.add(group)

        self.item = Item.objects.create(name="Keyboard",description="Mechanical Keyboard",quantity=5,category=self.category)

    def test_user_can_request_item(self):
        self.client.login(username="student", password="password")
        self.client.get(reverse('request_item', args=[self.item.id]))

        self.assertEqual(Request.objects.count(), 1)
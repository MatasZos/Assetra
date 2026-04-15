from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Request(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} requested {self.item}"
    
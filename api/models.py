from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Expense(models.Model):
    url = models.TextField(max_length=255)
    # response = models.JSONField()
    product = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expense")

    def __str__(self):
        return self.product

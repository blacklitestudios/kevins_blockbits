from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields here (optional)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    # Add these to resolve the conflict
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",  # Changed from default 'user_set'
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # Changed from default 'user_set'
        related_query_name="user",
    )

class Transaction(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_transactions', on_delete=models.CASCADE, default=1)
    receiver = models.ForeignKey(CustomUser, related_name='received_transactions', on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

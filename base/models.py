# importing necessary django classes
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import Group, Permission


ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('user', 'User'),
)

class customUser(AbstractUser):

    first_name = models.CharField('First Name of User', blank=True, max_length=20)
    last_name = models.CharField('Last Name of User', blank=True, max_length=20)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f'{self.username}'
		
from django.contrib.auth import get_user_model

# User = get_user_model()

class Transaction(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user.username} - {self.amount}"


  
      
	
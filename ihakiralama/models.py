from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class UAV(models.Model):
    uav_name = models.CharField(max_length=255)
    uav_brand = models.CharField(max_length=255)
    uav_model = models.CharField(max_length=255)
    uav_weight = models.DecimalField(max_digits=10, decimal_places=2)
    uav_range = models.DecimalField(max_digits=10, decimal_places=2)
    uav_quantity = models.PositiveIntegerField()
    daily_rental_fee = models.DecimalField(max_digits=10, decimal_places=2)

class Rent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)


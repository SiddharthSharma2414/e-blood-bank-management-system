from django.db import models
from django.contrib.auth.models import User

# Blood Bank Model
class BloodBank(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# Donor Model
class Donor(models.Model):
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    last_donation_date = models.DateField()

    def __str__(self):
        return self.name


# Blood Stock Model
class BloodStock(models.Model):
    hospital_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    units = models.IntegerField()
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.hospital_name


# Blood Request Model
class BloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    blood_group = models.CharField(max_length=5)
    quantity = models.IntegerField()
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
    ],
    default='Pending'
)

    def __str__(self):
        return f"{self.blood_group} - {self.city} - {self.contact}"
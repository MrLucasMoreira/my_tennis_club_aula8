from django.db import models
from plans.models import Plan

class Member(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, default=1)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    foto = models.ImageField(upload_to='images/', null=True)
    documento = models.FileField(null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

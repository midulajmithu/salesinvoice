from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class P_S_Info(models.Model):
    SorP=models.CharField(max_length=30,null=True)
    date=models.DateField(null=True, blank=True)
    mr_mh_no=models.CharField(max_length=30)
    item=models.CharField(max_length=30)
    unit_of_measure=models.CharField(max_length=30)
    quantity=models.IntegerField(null=True)
    supplier_name=models.CharField(max_length=30)
    project_no=models.CharField(max_length=30)
    invoice_no=models.CharField(max_length=30)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class stock(models.Model):
    item=models.CharField(max_length=30)
    P_quantity=models.IntegerField(null=True)
    S_quantity=models.IntegerField(null=True)
    stock_quantity=models.IntegerField(null=True)



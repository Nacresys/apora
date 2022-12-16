import datetime

from django.db import models

# Create your models here.
class orderlist(models.Model):
    id = models.IntegerField(primary_key=True)
    orderId = models.CharField(max_length=250)
    productId = models.IntegerField()
    product_name = models.CharField(max_length=250)
    quantity = models.IntegerField()
    status = models.IntegerField()
    qr = models.IntegerField()
    date = models.DateField()
    customer_name = models.CharField(max_length=250,default="NULL")
    address_city = models.CharField(max_length=150,default="NULL")
    class Meta:
        db_table = 'orderlist'

class product_master(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product = models.CharField(max_length=250)
    Batch = models.CharField(max_length=250)
    row = models.IntegerField()
    rack = models.IntegerField()
    shelf = models.IntegerField()
    stock_qty = models.IntegerField()
    class Meta:
        db_table = 'product_master'
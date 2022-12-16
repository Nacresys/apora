from django.db import models

# Create your models here.
class picklist_assignment(models.Model):
    id = models.IntegerField(primary_key=True)
    pickid = models.CharField(max_length=50)
    picker_id = models.IntegerField()
    productid = models.IntegerField()
    row = models.IntegerField()
    rack = models.IntegerField()
    shelf = models.IntegerField()
    status = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateField()
    class Met:
        db_table = 'picklist_assignment'
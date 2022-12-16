from django.db import models

# Create your models here.

class userreg(models.Model):
    id = models.IntegerField(primary_key=True)
    uname = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    pwd = models.CharField(max_length=100)
    role_id = models.IntegerField()

    class Meta:
        db_table = "usermaster"

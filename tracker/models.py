from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import PositiveIntegerField


# Create your models here.



class Category(models.Model):

    date = models.DateField(default=datetime.date.today)
    food = models.IntegerField(default=0)
    shopping = models.IntegerField(default=0)
    travel = models.IntegerField(default=0)
    others = models.IntegerField(default=0)
    current_user = models.ForeignKey(User,on_delete=models.CASCADE)



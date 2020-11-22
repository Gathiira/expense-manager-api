from django.db import models
from django.contrib.auth import get_user_model

from util.models import Timestamps

CATEGORY_OPTIONS = {
    ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
    ('RENT', 'RENT'),
    ('WIFI', 'WIFI'),
    ('FOOD', 'FOOD'),
    ('TRANSPORT', 'TRANSPORT'),
    ('OTHERS', 'OTHERS'),
}

SOURCE_OPTIONS = {
    ('SALARY', 'SALARY'),
    ('BUSINESS', 'BUSINESS'),
    ('SIDE_HUSTLE', 'SIDE_HUSTLE'),
    ('OTHERS', 'OTHERS'),
}


class ExpenseModel(Timestamps, models.Model):
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

class IncomeModel(Timestamps,models.Model):
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

from django.db import models
from django.contrib.auth.models import User
from enum import Enum


# Create your models here.
class FormFieldTypes(Enum):
    SINGLE_TEXT = 0
    MULTI_TEXT = 1
    DATE = 2
    CHECKBOX = 3
    
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class Licence(models.Model):
    name = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    absolute_max_tokens = models.PositiveIntegerField(default=0, blank=True)
    warning_max_tokens = models.PositiveIntegerField(default=0, blank=True)
    cost = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True)
    allowed_models = models.TextField(default='', blank=True)
    duration_days = models.PositiveIntegerField(help_text='Duration of the licence in days.', default=0, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    abn = models.CharField(max_length=20, blank=True)
    # company_image = models.ImageField(upload_to='images/')
    creation_date = models.DateTimeField(auto_now_add=True)

    billing_email = models.EmailField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    licence = models.ForeignKey(Licence, on_delete=models.SET_NULL, null=True)
    tokens_used = models.BigIntegerField(default=0, blank=True)
    monthly_tokens_used = models.IntegerField(default=0, blank=True)

    users = models.ManyToManyField(User, related_name='companies')


class Form(models.Model):
    name = models.CharField(max_length=100)
    parent_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    system_context = models.TextField(default='', blank=True)


class FormQuestion(models.Model):
    name = models.CharField(max_length=100)
    parent_form = models.ForeignKey(Form, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    field_type = models.PositiveSmallIntegerField(choices=FormFieldTypes.choices())
    prefill = models.CharField(max_length=100, blank=True)
    enabled = models.BooleanField(default=True)
from django.contrib import admin
from .models import Licence, Company, Form, FormQuestion

admin.site.register(Licence)
admin.site.register(Company)
admin.site.register(Form)
admin.site.register(FormQuestion)
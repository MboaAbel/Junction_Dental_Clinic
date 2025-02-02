from django.contrib import admin

# Register your models here.
from .models import Specialization, Page, Blog

# Register your models here.

admin.site.register(Specialization)
admin.site.register(Page)
admin.site.register(Blog)

from django.db import models
import string
import random
import uuid


def generate_service_id():
    alphanumeric = string.ascii_uppercase + string.digits
    return ''.join(random.choices(alphanumeric, k=6))


class Specialization(models.Model):
    service_code = models.CharField(default=generate_service_id, null=True,  max_length=6, )
    sname = models.CharField(max_length=100, null=True,)
    service_title = models.CharField(max_length=225, null=True,)
    service_image = models.ImageField(upload_to='services_image/', null=True, blank=True)
    service_logo = models.ImageField(upload_to='service_logo/', null=True, blank=True)
    service_price = models.IntegerField(null=True, blank=False)
    ratings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sname


class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle

class Blog(models.Model):
    soshi_user = models.CharField(max_length=100)
    blog_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    blog_title = models.CharField(max_length=250)
    blog_subtitle = models.CharField(max_length=250)
    caption = models.CharField(max_length=3000,editable=True)
    blog_image = models.ImageField(upload_to='profile_photos/', null=False, default='icon/bondijunction_dentalclinic_logo-300x258.jpg', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.blog_id}'
    

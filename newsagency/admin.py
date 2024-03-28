from django.contrib import admin

# Register your models here.

from .models import Login, Story, Author
admin.site.register(Login)
admin.site.register(Story)
admin.site.register(Author)



# ALLOWED_HOSTS = ['*']
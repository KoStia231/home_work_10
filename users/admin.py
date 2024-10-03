from django.contrib import admin

from users.models import User, PayMent

admin.site.register(User)  # Replace YourModel with your actual model name
admin.site.register(PayMent)  # Replace YourModel with your actual model name

# Register your models here.

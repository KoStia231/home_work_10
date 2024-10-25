from django.contrib import admin

from users.models import User, PayMent

admin.site.register(User)


@admin.register(PayMent)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'data_payment', 'method_payment',
        'sum_payment', 'status_payment', 'payment_id'
    )
    search_fields = ('user',)
    list_filter = ('user',)

# Register your models here.

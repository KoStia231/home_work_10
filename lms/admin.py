from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title',)
    list_filter = ('course',)


@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ('user', 'course', 'subscribed_at',)
    search_fields = ('user', 'course', 'subscribed_at',)
    list_filter = ('user', 'course', 'subscribed_at',)

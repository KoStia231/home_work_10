from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='название курса')
    description = models.TextField(verbose_name='описание курса')
    avatar = models.ImageField(verbose_name='превью', upload_to='course/')


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    avatar = models.ImageField(verbose_name='превью', upload_to='lesson/')
    video_link = models.URLField(verbose_name='ссылка на видео')





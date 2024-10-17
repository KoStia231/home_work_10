from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='название курса')
    description = models.TextField(verbose_name='описание курса')
    avatar = models.ImageField(verbose_name='превью', upload_to='course/')
    autor = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name='курс')
    avatar = models.ImageField(verbose_name='превью', upload_to='lesson/', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео')
    autor = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

# Generated by Django 4.2.2 on 2024-10-03 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_rename_name_course_title_rename_name_lesson_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'курс', 'verbose_name_plural': 'курсы'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lms.course', verbose_name='курс'),
        ),
    ]

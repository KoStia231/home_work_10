# Generated by Django 4.2.2 on 2024-10-03 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payment_course_alter_payment_lesson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'оплата', 'verbose_name_plural': 'оплаты'},
        ),
    ]

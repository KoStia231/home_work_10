# Generated by Django 4.2.2 on 2024-10-24 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payment_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_id',
        ),
    ]
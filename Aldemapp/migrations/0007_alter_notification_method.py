# Generated by Django 5.0.6 on 2025-01-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aldemapp', '0006_notification_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='method',
            field=models.CharField(choices=[('email', 'الارسال الى الإيميل'), ('site', 'الارسال الى المنصة')], default='site', max_length=10, verbose_name='طريقة الإرسال'),
        ),
    ]

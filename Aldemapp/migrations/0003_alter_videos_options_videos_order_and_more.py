# Generated by Django 5.0.6 on 2024-11-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aldemapp', '0002_alter_videos_video_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videos',
            options={'ordering': ['order'], 'verbose_name': 'فيديو', 'verbose_name_plural': 'فيديوهات'},
        ),
        migrations.AddField(
            model_name='videos',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='ترتيب الفيديو'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='thumbnail',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='thumbnails/', verbose_name='غلاف المقطع'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='video_file',
            field=models.FileField(blank=True, max_length=355, null=True, upload_to='videos/', verbose_name='الفيديو'),
        ),
    ]

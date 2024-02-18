# Generated by Django 5.0.2 on 2024-02-18 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название курса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses/', verbose_name='превью курса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание курса')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название урока')),
                ('description', models.TextField(verbose_name='описание урока')),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses/lessons/', verbose_name='превью урока')),
                ('link', models.URLField(blank=True, null=True, verbose_name='ссылка на видео')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='materials.course')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]
# Generated by Django 4.1.7 on 2023-02-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(),
        ),
    ]
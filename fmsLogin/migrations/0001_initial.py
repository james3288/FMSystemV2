# Generated by Django 4.2.2 on 2023-08-14 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200, verbose_name='Category')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
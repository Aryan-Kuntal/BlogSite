# Generated by Django 3.2.4 on 2021-09-25 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 3.1 on 2022-10-25 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0003_auto_20221024_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='gender',
            field=models.CharField(max_length=20),
        ),
    ]

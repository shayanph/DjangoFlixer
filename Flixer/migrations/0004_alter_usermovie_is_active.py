# Generated by Django 3.2.5 on 2021-08-03 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flixer', '0003_usermovie_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermovie',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 3.2.5 on 2021-08-05 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flixer', '0004_alter_usermovie_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating_value',
            field=models.IntegerField(),
        ),
    ]

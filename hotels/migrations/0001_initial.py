# Generated by Django 4.0.4 on 2022-05-16 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HotelPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_code', models.CharField(max_length=20)),
                ('check_in_date', models.DateField()),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('median_price', models.FloatField()),
            ],
        ),
    ]

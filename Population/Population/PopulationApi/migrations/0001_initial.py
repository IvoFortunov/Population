# Generated by Django 2.2.28 on 2022-05-05 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='countryCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryCode', models.CharField(max_length=3)),
                ('countryName', models.CharField(max_length=255)),
            ],
        ),
    ]

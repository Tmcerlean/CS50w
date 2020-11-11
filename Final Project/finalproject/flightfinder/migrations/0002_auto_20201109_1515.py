# Generated by Django 3.1.2 on 2020-11-09 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightfinder', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='currency',
            new_name='userCurrency',
        ),
        migrations.AddField(
            model_name='flight',
            name='inboundDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='userCountry',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='flight',
            name='userLocale',
            field=models.CharField(default=None, max_length=50),
        ),
    ]

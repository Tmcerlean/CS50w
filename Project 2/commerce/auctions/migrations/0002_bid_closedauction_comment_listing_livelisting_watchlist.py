# Generated by Django 3.1.2 on 2020-10-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('bid', models.DecimalField(decimal_places=2, default=None, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='ClosedAuction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller', models.CharField(max_length=64)),
                ('winner', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('winningbid', models.DecimalField(decimal_places=2, default=None, max_digits=5)),
                ('dateended', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('comment', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('datelisted', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('initialprice', models.IntegerField(default=None)),
                ('currentprice', models.IntegerField()),
                ('image', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LiveListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('listingid', models.IntegerField()),
                ('image', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
            ],
        ),
    ]

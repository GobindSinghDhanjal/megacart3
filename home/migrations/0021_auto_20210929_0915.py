# Generated by Django 3.2.3 on 2021-09-29 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealsoftheday',
            name='description3',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='dealsoftheday',
            name='description4',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='dealsoftheday',
            name='description5',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='dealsoftheday',
            name='offer1',
            field=models.CharField(blank=True, default='Bank Offer 10% off on any Debit/Credit Cards, up to ₹1500. On orders of ₹5000 and above', max_length=300),
        ),
        migrations.AddField(
            model_name='dealsoftheday',
            name='offer2',
            field=models.CharField(blank=True, default='Get a Google Home Mini at just ₹1,499 on purchase of select laptops, TVs, ACs and mobile phones', max_length=300),
        ),
        migrations.AlterField(
            model_name='dealsoftheday',
            name='description1',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='dealsoftheday',
            name='description2',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='dealsoftheday',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-30 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Receipt', '0002_alter_receipt_payment_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='مبلغ'),
        ),
    ]

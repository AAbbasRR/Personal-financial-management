# Generated by Django 4.0.4 on 2022-05-24 07:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstallmentPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True, verbose_name='زمان پرداخت')),
            ],
            options={
                'verbose_name': 'پرداخت قسط',
                'verbose_name_plural': 'پرداختی های اقساط',
            },
        ),
        migrations.CreateModel(
            name='Installments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='مبلغ')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ شروع قسط')),
                ('count', models.IntegerField(verbose_name='تعداد اقساط')),
                ('type', models.CharField(choices=[('DAY', 'روزانه'), ('WEK', 'هفتگی'), ('MON', 'ماهانه'), ('YEA', 'سالیانه')], default='MON', max_length=3, verbose_name='نوع پرداخت')),
                ('status', models.CharField(choices=[('CLS', 'بایگانی'), ('OPN', 'جاری')], default='OPN', max_length=3, verbose_name='وضعیت')),
            ],
            options={
                'verbose_name': 'قسط',
                'verbose_name_plural': 'اقساط',
            },
        ),
    ]

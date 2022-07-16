from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from app_Utils.models import BaseAmount, BaseDescription

from jalali_date import datetime2jalali

User = get_user_model()


class Wallet(BaseAmount):
    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول ها'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="کاربر"
    )

    def __str__(self) -> str:
        return self.user.email


class Transaction(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول ها'
        ordering = ['created_date']

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="کاربر"
    )

    Bill = "BIL"
    Check = "CHK"
    DebtAndDemand = "DBM"
    Installments = "INS"
    Receipt = "RCP"
    Saving = "SVG"
    More = "MRE"
    type_choices = [
        (Bill, "درآمد"),
        (Check, "چک"),
        (DebtAndDemand, "بدهی و طلب"),
        (Installments, "قسط"),
        (Receipt, "قبض"),
        (Saving, "پس انداز"),
        (More, "اضافی"),
    ]
    type = models.CharField(
        max_length=3,
        choices=type_choices,
        default=More,
        verbose_name="نوع تراکنش"
    )
    reference_id = models.IntegerField(
        null=True,
        verbose_name='ایدی منبع'
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='تاریخ ایجاد'
    )
    Addition = "ADT"
    Deduction = "DET"
    choice_condition = [
        (Addition, "اضافه"),
        (Deduction, "کسر")
    ]
    condition = models.CharField(
        max_length=3,
        choices=choice_condition,
        default=Addition,
        verbose_name="وضعیت تراکنش"
    )

    def __str__(self) -> str:
        return self.user.email

    def get_jalali_created_date_time(self):
        return datetime2jalali(self.created_date)

    def get_jalali_created_date(self):
        return datetime2jalali(self.created_date).date()

    def get_jalali_created_time(self):
        return datetime2jalali(self.created_date).time()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.condition == "ADT":
            try:
                Wallet.objects.filter(user=self.user).update(amount=models.F('amount') + self.amount)
            except Wallet.DoesNotExist:
                Wallet.objects.create(user=self.user, amount=self.amount)
        else:
            try:
                Wallet.objects.filter(user=self.user).update(amount=models.F('amount') - self.amount)
            except Wallet.DoesNotExist:
                Wallet.objects.create(user=self.user, amount=-self.amount)
        return super(Transaction, self).save(force_insert, force_update, using, update_fields)

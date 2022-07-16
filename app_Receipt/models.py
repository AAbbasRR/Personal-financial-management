from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from jalali_date import datetime2jalali

from app_Utils.models import BaseAmount, BaseDescription
from app_Transactions.models import Transaction


class Receipt(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = "قبض"
        verbose_name_plural = "قبوض"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="کاربر"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="اسم قبض"
    )
    payment_date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="زمان پرداخت"
    )
    tracking_code = models.CharField(
        max_length=50,
        verbose_name="کد رهگیری"
    )
    Phone = "PHN"
    Electric = "ELC"
    Water = "WTR"
    Gas = "GAS"
    Tax = "TAX"
    receipt_type = [
        (Phone, "تلفن"),
        (Electric, "برق"),
        (Water, "آب"),
        (Gas, "گاز"),
        (Tax, "مالیات"),
    ]
    type = models.CharField(
        max_length=3,
        choices=receipt_type,
        verbose_name="نوع قبض"
    )

    def __str__(self) -> str:
        return f"{self.user.email} - {self.name}"

    def get_jalali_payment_date_time(self):
        return datetime2jalali(self.payment_date_time)

    def get_jalali_payment_date(self):
        return datetime2jalali(self.payment_date_time).date()

    def get_jalali_payment_time(self):
        return datetime2jalali(self.payment_date_time).time()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        Transaction.objects.create(user=self.user, type="RCP", reference_id=self.id, condition="DET", amount=self.amount, description=self.description)
        return super(Receipt, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        Transaction.objects.create(user=self.user, type="RCP", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
        return super(Receipt, self).delete(using, keep_parents)

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from jalali_date import date2jalali

from app_Utils.models import BaseAmount, BaseDescription
from app_Transactions.models import Transaction


class Check(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = "چک"
        verbose_name_plural = "چک ها"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        verbose_name="سازنده"
    )

    person = models.CharField(
        max_length=100,
        verbose_name="نام شخص"
    )
    check_number = models.IntegerField(
        verbose_name="شماره چک"
    )
    check_date = models.DateField(
        default=timezone.now,
        verbose_name="تاریخ وصول"
    )
    Payment = "PAY"
    Received = "REC"
    check_type_choices = [
        (Payment, "پرداختی"),
        (Received, "دریافتی")
    ]
    type = models.CharField(
        max_length=3,
        choices=check_type_choices,
        default=Payment,
        verbose_name="نوع"
    )
    During = "DUR"
    Successful = "SUC"
    Failure = "FIL"
    check_status_choices = [
        (During, "در جریان"),
        (Successful, "وصول شده"),
        (Failure, "عدم وصول")
    ]
    status = models.CharField(
        max_length=3,
        choices=check_status_choices,
        default=During,
        verbose_name="وضعیت"
    )

    def __str__(self) -> str:
        return f"{self.user.email} - {self.person} - check"

    def get_jalali_check_date(self):
        return date2jalali(self.check_date)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.status == "SUC":
            if self.type == "PAY":
                Transaction.objects.create(user=self.user, type="CHK", reference_id=self.id, condition="DET", amount=self.amount, description=self.description)
            else:
                Transaction.objects.create(user=self.user, type="CHK", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
        return super(Check, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.status == "SUC":
            if self.type == "PAY":
                Transaction.objects.create(user=self.user, type="CHK", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
            else:
                Transaction.objects.create(user=self.user, type="CHK", reference_id=self.id, condition="DET", amount=self.amount, description=self.description)
        return super(Check, self).delete(using, keep_parents)

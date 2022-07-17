from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from jalali_date import date2jalali

from app_Utils.models import BaseDescription, BaseAmount
from app_Transactions.models import Transaction


class DebtAndDemand(BaseDescription, BaseAmount):
    class Meta:
        verbose_name = "بدهی و طلب"
        verbose_name_plural = f"{verbose_name} ها"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        verbose_name="کاربر"
    )
    person = models.CharField(
        max_length=100,
        verbose_name="نام شخص"
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name="تاریخ شروع"
    )
    end_date = models.DateField(
        verbose_name="تاریخ پایان",
        null=True,
        blank=True
    )
    Debt = "DEB"
    Demand = "DEM"
    type_choices = [
        (Debt, "بدهی"),
        (Demand, "طلب"),
    ]
    type = models.CharField(
        max_length=3,
        choices=type_choices,
        default=Debt,
        verbose_name="نوع"
    )
    Closed = "CLS"
    Opened = "OPN"
    status_choices = [
        (Closed, "بایگانی"),
        (Opened, "جاری")
    ]
    status = models.CharField(
        max_length=3,
        choices=status_choices,
        default=Opened,
        verbose_name="وضعیت"
    )

    def __str__(self) -> str:
        return f"{self.user.email} - {self.type}"

    def get_jalali_start_date(self):
        return date2jalali(self.start_date)

    def get_jalali_end_date(self):
        return date2jalali(self.end_date)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        dbm_object = super(DebtAndDemand, self).save(force_insert, force_update, using, update_fields)
        if self.status == "OPN":
            if self.type == "DEB":
                Transaction.objects.create(user=self.user, type="DBM", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
            else:
                Transaction.objects.create(user=self.user, type="DBM", reference_id=self.id, condition="DET", amount=self.amount, description=self.description)
        else:
            if self.type == "DEB":
                Transaction.objects.create(user=self.user, type="DBM", reference_id=self.id, condition="DET", amount=self.amount, description=self.description)
            else:
                Transaction.objects.create(user=self.user, type="DBM", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
        return dbm_object

    def delete(self, using=None, keep_parents=False):
        if self.status == "OPN":
            if self.type == "DEB":
                Transaction.objects.create(user=self.user, type="DBM", reference_id=self.id, condition="DET", amount=self.amount, description=self.description)
            else:
                Transaction.objects.create(user=self.user, type="DBM", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
        return super(DebtAndDemand, self).delete(using, keep_parents)

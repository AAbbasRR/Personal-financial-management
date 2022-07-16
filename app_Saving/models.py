from django.db import models
from django.contrib.auth import get_user_model

from jalali_date import date2jalali, datetime2jalali

from app_Utils.models import BaseAmount, BaseDescription
from app_Transactions.models import Transaction


class Saving(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = "صندوق پس انداز"
        verbose_name_plural = "صندوق های پس انداز"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="کاربر"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="نام"
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    def __str__(self) -> str:
        return f"{self.user.email} - {self.name}"

    def get_created_date(self):
        return date2jalali(self.created)

    def get_payment_count(self):
        return self.app_saving_savingpaymentlog_related.count()

    def get_payment_objects(self):
        return self.app_saving_savingpaymentlog_related.all()

    def delete(self, using=None, keep_parents=False):
        Transaction.objects.create(user=self.user, type="SVG", reference_id=self.id, condition="ADT", amount=self.amount, description=self.description)
        return super(Saving, self).delete(using, keep_parents)


class SavingPaymentLog(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = "پرداخت پس انداز"
        verbose_name_plural = "پرداختی های پس انداز"

    saving = models.ForeignKey(
        Saving,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="صندوق پس انداز"
    )

    payment_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان پرداخت"
    )

    Withdrawal = "WID"
    Deposit = "DEP"
    type_choices = [
        (Withdrawal, "برداشت"),
        (Deposit, "واریز"),
    ]
    type = models.CharField(
        max_length=3,
        choices=type_choices,
        default=Deposit,
        verbose_name="نوع پرداخت"
    )

    def __str__(self) -> str:
        return f"{self.saving} - payment"

    def get_jalali_payment_date_time(self):
        return datetime2jalali(self.payment_time)

    def get_jalali_payment_data(self):
        return datetime2jalali(self.payment_time).date()

    def get_jalali_payment_time(self):
        return datetime2jalali(self.payment_time).time()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.type == "DEP":
            self.saving.amount = models.F('amount') + self.amount
            Transaction.objects.create(user=self.saving.user, type="SVG", reference_id=self.saving.id, condition="DET", amount=self.amount, description=self.description)
        else:
            self.saving.amount = models.F('amount') - self.amount
            Transaction.objects.create(user=self.saving.user, type="SVG", reference_id=self.saving.id, condition="ADT", amount=self.amount, description=self.description)
        self.saving.save()
        return super(SavingPaymentLog, self).save(force_insert, force_update, using, update_fields)

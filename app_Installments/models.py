from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from jalali_date import date2jalali, datetime2jalali

from app_Utils.models import BaseAmount, BaseDescription
from app_Transactions.models import Transaction


def restrict_amount(pk):
    installment_object = Installments.objects.filter(id=pk).first()
    if installment_object:
        if installment_object.app_installments_installmentpayments_related.count() >= installment_object.count:
            raise ValidationError(f'Installment already has maximal amount of rounds ({installment_object.count})')


class Installments(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = "قسط"
        verbose_name_plural = "اقساط"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="کاربر"
    )
    title = models.CharField(
        max_length=50,
        verbose_name="عنوان"
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name="تاریخ شروع قسط"
    )
    count = models.IntegerField(
        verbose_name="تعداد اقساط"
    )
    Daily = "DAY"
    Weekly = "WEK"
    Monthly = "MON"
    Yearly = "YEA"
    type_choices = [
        (Daily, "روزانه"),
        (Weekly, "هفتگی"),
        (Monthly, "ماهانه"),
        (Yearly, "سالیانه"),
    ]
    type = models.CharField(
        max_length=3,
        choices=type_choices,
        default=Monthly,
        verbose_name="نوع پرداخت"
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
        return f"{self.user.email} - {self.title}"

    def get_jalali_start_date(self):
        return date2jalali(self.start_date)

    def get_total_amount(self):
        return self.amount * self.count

    def get_installment_payment_percent(self):
        return int((self.app_installments_installmentpayments_related.count() * 100) / self.count)

    def get_installment_payment_objects(self):
        return self.app_installments_installmentpayments_related.all()

    def get_payment_remaining_number(self):
        return self.count - self.app_installments_installmentpayments_related.count()

    def delete(self, using=None, keep_parents=False):
        if self.status == "CLS":
            Transaction.objects.create(user=self.user, type="INS", reference_id=self.id, condition="ADT", amount=self.app_installments_installmentpayments_related.count() * self.amount, description=self.description)
        return super(Installments, self).delete(using, keep_parents)


class InstallmentPayments(models.Model):
    class Meta:
        verbose_name = "پرداخت قسط"
        verbose_name_plural = "پرداختی های اقساط"

    installment = models.ForeignKey(
        Installments,
        on_delete=models.CASCADE,
        validators=(restrict_amount,),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="قسط"
    )
    payment_date_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان پرداخت"
    )

    def __str__(self) -> str:
        return f"{self.installment.user.email} - {self.installment.title}"

    def get_jalali_payment_data_time(self):
        return datetime2jalali(self.payment_date_time)

    def get_jalali_payment_data(self):
        return datetime2jalali(self.payment_date_time).date()

    def get_jalali_payment_time(self):
        return datetime2jalali(self.payment_date_time).time()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.installment.status == "OPN":
            Transaction.objects.create(user=self.installment.user, type="INS", reference_id=self.installment.id, condition="DET", amount=self.installment.amount, description=self.installment.description)
        return super(InstallmentPayments, self).save(force_insert, force_update, using, update_fields)

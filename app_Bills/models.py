from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from app_Utils.models import BaseAmount, BaseDescription

from jalali_date import date2jalali


class Bill(BaseAmount, BaseDescription):
    class Meta:
        verbose_name = "منبع خرج"
        verbose_name_plural = "منابع خرج"

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        verbose_name="کاربر"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="نام منبع"
    )
    receive_date = models.DateField(
        default=timezone.now,
        verbose_name="تاریخ شروع دریافت"
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
        verbose_name="نوع دریافت"
    )

    def __str__(self) -> str:
        return f"{self.user.email} - {self.name}"

    def get_jalali_receive_date(self):
        return date2jalali(self.receive_date)

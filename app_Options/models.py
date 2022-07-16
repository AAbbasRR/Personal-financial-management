from django.db import models
from django.contrib.auth import get_user_model


def unique_type_validator(pk):
    print(pk)


class NotificationOptions(models.Model):
    class Meta:
        verbose_name = 'تنظیمات اطلاع رسانی'
        verbose_name_plural = 'تنظیمات اطلاع رسانی ها'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name='%(app_label)s_%(class)ss',
        verbose_name="کاربر"
    )
    CHECK = "CHK"
    BILL = "BIL"
    INSTALLMENT = "INS"
    DEBTANDDEMAND = "DBM"
    type_choices = [
        (CHECK, "چک"),
        (BILL, "منبع خرج"),
        (INSTALLMENT, "قسط"),
        (DEBTANDDEMAND, "بدهی و طلب"),
    ]
    type = models.CharField(
        max_length=3,
        choices=type_choices,
        default=INSTALLMENT,
        validators=(unique_type_validator,),
        verbose_name="دسته اطلاع رسانی"
    )
    WEEK = "WEK"
    TWODAY = "TDY"
    DAY = "DAY"
    time_choices = [
        (WEEK, "۱ هفته قبل"),
        (TWODAY, "۲ روز قبل"),
        (DAY, "۱ روز قبل")
    ]
    time_notice = models.CharField(
        max_length=3,
        choices=time_choices,
        default=DAY,
        verbose_name="زمان اطلاع رسانی"
    )
    EMAIL = "EML"
    PANEL = "PNL"
    notice_choices = [
        (EMAIL, "ایمیل"),
        (PANEL, "پنل کاربری"),
    ]
    notice_type = models.CharField(
        max_length=3,
        choices=notice_choices,
        default=PANEL,
        verbose_name="نوع اطلاع رسانی"
    )

    def __str__(self) -> str:
        return f'{self.user.email} - {self.type}'

from django.db import models


class BaseAmount(models.Model):
    class Meta:
        abstract = True

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ"
    )


class BaseDescription(models.Model):
    class Meta:
        abstract = True

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="توضیجات"
    )

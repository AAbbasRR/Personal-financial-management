from django import forms

from jalali_date.fields import SplitJalaliDateTimeField
from jalali_date.widgets import AdminSplitJalaliDateTime

from .models import Receipt

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


class ReceiptCreateForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = [
            'name',
            'amount',
            'payment_date_time',
            'type',
            'tracking_code',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(ReceiptCreateForm, self).__init__(*args, **kwargs)
        self.fields['payment_date_time'] = SplitJalaliDateTimeField(
            label='زمان پرداخت',
            widget=AdminSplitJalaliDateTime
        )
        self.fields['payment_date_time'].widget.widgets[0].attrs.update({'class': 'jalali_date-date form-control', 'placeholder': 'تاریخ پرداخت'})
        self.fields['payment_date_time'].widget.widgets[1].attrs.update({'class': 'form-control', 'placeholder': 'زمان پرداخت'})

    def get_type_options(self):
        return receipt_type

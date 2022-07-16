from django import forms

from jalali_date.fields import SplitJalaliDateTimeField
from jalali_date.widgets import AdminSplitJalaliDateTime

from .models import Transaction

Addition = "ADT"
Deduction = "DET"
choice_condition = [
    (Addition, "اضافه"),
    (Deduction, "کسر")
]


class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'type',
            'amount',
            'description',
            'condition',
            'created_date'
        ]

    def __init__(self, *args, **kwargs):
        super(TransactionCreateForm, self).__init__(*args, **kwargs)
        self.fields['created_date'] = SplitJalaliDateTimeField(
            label='زمان ایجاد',
            widget=AdminSplitJalaliDateTime
        )
        self.fields['created_date'].widget.widgets[0].attrs.update({'class': 'jalali_date-date form-control', 'placeholder': 'تاریخ ایجاد'})
        self.fields['created_date'].widget.widgets[1].attrs.update({'class': 'form-control', 'placeholder': 'زمان ایجاد'})

    def get_condition_options(self):
        return choice_condition

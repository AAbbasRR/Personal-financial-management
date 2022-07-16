from django import forms

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import Bill

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


class BillCreateForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'name',
            'receive_date',
            'amount',
            'type',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(BillCreateForm, self).__init__(*args, **kwargs)
        self.fields['receive_date'] = JalaliDateField(
            label='تاریخ شروع دریافت',
            widget=AdminJalaliDateWidget
        )
        self.fields['receive_date'].widget.attrs.update({'class': 'jalali_date-date form-control', 'placeholder': 'تاریخ شروع دریافت'})

    def get_type_options(self):
        return type_choices

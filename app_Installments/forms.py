from django import forms

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import Installments

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


class InstallmentsCreateForm(forms.ModelForm):
    class Meta:
        model = Installments
        fields = [
            'title',
            'amount',
            'start_date',
            'count',
            'type',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(InstallmentsCreateForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = JalaliDateField(
            label='تاریخ تولد',
            widget=AdminJalaliDateWidget
        )
        self.fields['start_date'].widget.attrs.update({'class': 'jalali_date-date form-control', 'placeholder': 'تاریخ شروع قسط'})

    def get_type_options(self):
        return type_choices

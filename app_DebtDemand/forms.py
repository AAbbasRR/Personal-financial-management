from django import forms

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import DebtAndDemand


class DebtDemandCreateForm(forms.ModelForm):
    class Meta:
        model = DebtAndDemand
        fields = [
            'person',
            'amount',
            'start_date',
            'description',
            'type',
        ]

    def __init__(self, *args, **kwargs):
        super(DebtDemandCreateForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = JalaliDateField(
            label='تاریخ شروع',
            widget=AdminJalaliDateWidget
        )
        self.fields['start_date'].widget.attrs.update({'class': 'jalali_date-date form-control', 'placeholder': 'تاریخ شروع'})

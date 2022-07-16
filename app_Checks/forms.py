from django import forms

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import Check


class CheckCreateForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = [
            'person',
            'amount',
            'check_number',
            'check_date',
            'description',
            'type',
        ]

    def __init__(self, *args, **kwargs):
        super(CheckCreateForm, self).__init__(*args, **kwargs)
        self.fields['check_date'] = JalaliDateField(
            label='تاریخ',
            widget=AdminJalaliDateWidget
        )
        self.fields['check_date'].widget.attrs.update({'class': 'jalali_date-date form-control', 'placeholder': 'تاریخ'})

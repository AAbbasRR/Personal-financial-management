from django import forms

from .models import Saving, SavingPaymentLog


class SavingCreateForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = [
            'name',
            'description'
        ]


class SavingPaymentCreateForm(forms.ModelForm):
    class Meta:
        model = SavingPaymentLog
        fields = [
            'amount',
            'type',
            'description'
        ]

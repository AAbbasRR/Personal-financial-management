from django import forms

from .models import NotificationOptions

WEEK = "WEK"
TWODAY = "TDY"
DAY = "DAY"
time_choices = [
    (WEEK, "۱ هفته قبل"),
    (TWODAY, "۲ روز قبل"),
    (DAY, "۱ روز قبل")
]
EMAIL = "EML"
PANEL = "PNL"
notice_choices = [
    (EMAIL, "ایمیل"),
    (PANEL, "پنل کاربری"),
]


class NotificationOptionsCreateForm(forms.ModelForm):
    class Meta:
        model = NotificationOptions
        fields = [
            'type',
            'time_notice',
            'notice_type',
        ]

    def __init__(self, *args, **kwargs):
        super(NotificationOptionsCreateForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['time_notice'].required = False
        self.fields['notice_type'].required = False

    def get_time_notice_options(self):
        return time_choices

    def get_notice_choices_options(self):
        return notice_choices
